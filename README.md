# Snake Data Collection

## Usage
Run the scripts in following order:
1. `python species_scraper`
2. `python inaturalist_data`
3. `python data_visualization`

## Directory Structure
`data_visualization/` - contains script for visualizing the dataset by loading JSON files with image URLs from `inaturalist_data/`, counting images from *static* and *open data* sources of iNaturalist, and generating a grouped bar chart to compare image counts per species.

`inaturalist_data/` - contains script for reading a list of snake species, retrieving image URLs from iNaturalist using the API, and saves them in JSON files.

`species_scraper/` - contains a script that scrapes snake species names from iNaturalist guide and saves them in a file.
