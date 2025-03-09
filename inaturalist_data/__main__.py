import json
import os
import queue
import threading
from pyinaturalist import Observation, enable_logging, get_observations
from rich import print
from time import sleep


# API rate limit avoidance parameters
# Please adjust to optimal values
CONCURRENT_REQUESTS = 60
SLEEP_AFTER_REQUEST = 60


enable_logging()


def read_species_list(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_to_JSON(data, filename):
    existing_data = []

    # Check if the file exists and is not empty
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)

    # Append new data, avoiding duplicates
    for url in data:
        if url not in existing_data:
            existing_data.append(url)
        else:
            print(f"URL already exists: {url}")

    # Write the updated list back to the file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    print(f"Data successfully added to {filename}")


def fetch_all_observations(taxon_name):
    all_observations = []
    page = 1
    per_page = 100  # Maximum allowed per request: 100

    while True:
        print(f"Fetching page {page} for {taxon_name}...")
        response = get_observations(
            taxon_name=taxon_name,
            photos=True,
            page=page,
            per_page=per_page,
        )
        sleep(SLEEP_AFTER_REQUEST)
        observations = Observation.from_json_list(response)

        if not observations:
            break

        all_observations.extend(observations)
        page += 1  # Go to the next page

    return all_observations


def modify_image_size(photo_url, former_size, new_size):
    """
    square → Small square thumbnail (75x75 px)
    small → Small size (240px)
    medium → Medium size (500px)
    large → Large size (1024px)
    original → Full-size image
    """
    return photo_url.replace(former_size, new_size)


def fetch_photo_urls(observations):
    photo_urls = []
    for obs in observations:
        for photo in obs.photos:
            modified_url = modify_image_size(photo.url, "square", "original")
            photo_urls.append(modified_url)
    return photo_urls


def _fetch(species, threads_queue):
    observations = fetch_all_observations(species)
    photo_urls = fetch_photo_urls(observations)

    print(f"Number of observations: {len(observations)}")
    print(f"Number of photo URLs: {len(photo_urls)}")

    filename = os.path.join(
        "data",
        "snake_photos",
        f"{species.lower().replace(' ', '_')}_photo_urls.json",
    )
    os.makedirs(os.path.join("data", "snake_photos"), exist_ok=True)

    save_to_JSON(photo_urls, filename)
    threads_queue.get()  # Pop queue


if __name__ == "__main__":
    filename = os.path.join("data", "snake_species.json")
    species_list = read_species_list(filename)
    threads = []

    # Queue is needed to limit the concurrent threads running at the same time
    # to avoid API rate limit
    threads_queue = queue.Queue(CONCURRENT_REQUESTS)

    for species in species_list:
        t = threading.Thread(target=_fetch, args=(species, threads_queue))
        threads_queue.put(t)  # Will block if queue is full
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
