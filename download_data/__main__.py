import os
import json
import requests

def load_snake_data(directory_path, snake_species):
    file_path = os.path.join(directory_path, f"{snake_species}_photo_urls.json")

    if not os.path.exists(file_path):
        print(f"Warning: No data file found for {snake_species}. Skipping...")
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(save_path, "wb") as img_file:
            img_file.write(response.content)

        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False

def download_snake_data(directory_path, snakes_list):
    for snake_species in snakes_list:
        data = load_snake_data(directory_path, snake_species)
        if not data:
            continue

        print(f"{snake_species}: {len(data)} photos found.")

        # Create directory to save images
        save_dir = os.path.join("data", "snakes", snake_species)
        os.makedirs(save_dir, exist_ok=True)

        # Download images
        for index, url in enumerate(data):
            file_extension = url.split(".")[-1].split("?")[0]  # Extract file extension
            image_path = os.path.join(save_dir, f"{index}.{file_extension}")

            if download_image(url, image_path):
                print(f"✔ Downloaded {snake_species} image {index + 1}/{len(data)}")

    print("✅ Download complete.")

if __name__ == "__main__":
    snakes_list = [
        "naja_sumatrana",
        "trimeresurus_flavomaculatus",
    ]
    directory_path = os.path.join("data", "snake_photos")

    download_snake_data(directory_path, snakes_list)
