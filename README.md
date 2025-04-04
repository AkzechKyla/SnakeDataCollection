# Snake Data Collection

## Usage
Run the scripts depending on what you need:
1. `python species_scraper`
2. `python inaturalist_data`
3. `python download_data`
4. `python data_visualization`
5. `python rename_data`

## Directory Structure
`data_visualization/` - contains script for visualizing the dataset by loading JSON files with image URLs from `inaturalist_data/`, counting images from *static* and *open data* sources of iNaturalist, and generating a grouped bar chart to compare image counts per species.

`download_data/` - contains scripts to download images from the URLs stored in the JSON files generated by `inaturalist_data/`.

`inaturalist_data/` - contains script for reading a list of snake species, retrieving image URLs from iNaturalist using the API, and saves them in JSON files.

`species_scraper/` - contains a script that scrapes snake species names from iNaturalist guide and saves them in a file.

`rename_data/` - contains a script for renaming image files sequentially.
