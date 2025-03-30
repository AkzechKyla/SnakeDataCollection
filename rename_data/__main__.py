import os

if __name__ == "__main__":
    directory_dict = {
        "Gervais Worm Snake": 0,
        "Reddish Rat Snake": 0,
        "Philippine Cobra": 0,
        "Smooth-Scaled Mountain Rat Snake": 0
    }
    directory_path = os.path.join("data", "snakes")

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if filename in directory_dict:
            start_count = directory_dict[filename]

            if os.path.isdir(file_path):
                for file in os.listdir(file_path):
                    src = os.path.join(file_path, file)
                    dst = os.path.join(file_path, f"{start_count}.jpg")

                    os.rename(src, dst)
                    start_count += 1

            print(f"Reading directory: {file_path}")
