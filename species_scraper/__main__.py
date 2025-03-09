import os
import requests
import json
from bs4 import BeautifulSoup


def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return None
    return response.text


def extract_snake_species(soup):
    snake_species = []

    for div in soup.find_all("div", class_="col-xs-3"):
        scientific_name = div.find("small")
        common_name = div.find("h5").find("a") if div.find("h5") else None

        if scientific_name and scientific_name.find("i"):
            snake_species.append(scientific_name.find("i").text.strip())
        elif common_name:
            snake_species.append(common_name.text.strip())

    return snake_species


def scrape_snake_species(urls):
    all_snake_species = []

    for url in urls:
        page_content = fetch_page_content(url)
        if not page_content:
            continue

        soup = BeautifulSoup(page_content, "html.parser")
        all_snake_species.extend(extract_snake_species(soup))

    return all_snake_species


def save_to_JSON(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    urls = [
        "https://www.inaturalist.org/guides/11042?page=1&view=grid",
        "https://www.inaturalist.org/guides/11042?page=2&view=grid",
    ]

    snake_species = scrape_snake_species(urls)

    if snake_species:
        print("\n".join(snake_species))
        print(f"Total: {len(snake_species)}")

        filename = os.path.join("data", "snake_species.json")
        os.makedirs("data", exist_ok=True)  # Create 'data' folder

        save_to_JSON(snake_species, filename)
    else:
        print("No snake was found.")
