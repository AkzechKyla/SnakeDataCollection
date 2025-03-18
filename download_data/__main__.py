import os
import json
import requests

def download_snake_data(directory_path, snakes_list):
    """Load raw JSON data for each snake species from files."""
    data_dict = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            snake_species = filename.replace("_photo_urls.json", "")

            if snake_species in snakes_list:
                file_path = os.path.join(directory_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                data_dict[snake_species] = data

                # Create directory to save images
                save_dir = os.path.join("data", "snakes", snake_species)
                os.makedirs(save_dir, exist_ok=True)

                # Download images
                for index, url in enumerate(data):
                    try:
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

                        # Save image file
                        file_extension = url.split(".")[-1].split("?")[0]  # Get file extension
                        image_path = os.path.join(save_dir, f"{index}.{file_extension}")

                        with open(image_path, "wb") as img_file:
                            img_file.write(response.content)

                        print(f"Downloaded {snake_species} image {index + 1}/{len(data)}")

                    except requests.exceptions.RequestException as e:
                        print(f"Failed to download {url}: {e}")

                data_dict[snake_species] = data

    print("Download complete.")

if __name__ == "__main__":
    snakes_list = [
        "ptyas_luzonensis",
    ]

    directory_path = os.path.join("data", "snake_photo_urls")
    download_snake_data(directory_path, snakes_list)
