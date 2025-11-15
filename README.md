# Logo_Similarity
Match and group websites by the similarity of their logos.
[Project presentation](https://docs.google.com/presentation/d/1SH6BkHShoCD6f0i2pKnsA5Fwj04GacLj/edit?usp=sharing&ouid=112555544588146967388&rtpof=true&sd=true)

## Description
This project is designed to extract logos from a list of websites and analyze them in order to identify visual similarities between brands. By downloading the logos, converting them to a standardized format, and generating perceptual hashes, it allows for efficient comparison of logo designs, detecting resemblances, and grouping brands with similar visual identities. This tool is especially useful for market research, brand monitoring, or building datasets for machine learning applications involving logo recognition and similarity detection.

## find_logo.py – Logo Extraction Module
The `find_logo.py` module is responsible for locating and retrieving logos from websites. It uses multiple strategies to maximize the chances of finding the correct logo:

- **Favicon and icon links**  

- **Image tags with keywords**  

- **Container and header search**  
  Looks inside `<header>` or `<nav>` sections and other container elements (`div`, `section`, `a`, `figure`, `span`) for potential logos.

- **SVG handling**  
  Detects inline SVG logos and converts them to PNG using [cairosvg](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)..

- **Storage**  
  Saves logos in the `logos/` 

The module iterates through multiple possible sources and attributes (`src`, `data-src`, `data-lazy`, `srcset`) to ensure the logo is found even if it is loaded dynamically or lazily. It returns the path of the saved PNG logo, or `None` if no logo could be found.

## logo_images.py – Logo Image Processing
The `logo_images.py` functionality is responsible for downloading, saving, and processing logo images once they are located on a website. Its main responsibilities include:

- **Downloading images**  
  Fetches images from URLs using HTTP requests.

- **Image Standardization**  
  Converts images to a consistent format (RGBA) to prevent issues when computing perceptual hashes.

- **Hash Generation**  
  Uses `imagehash` to compute perceptual hashes (`phash`) for logo comparison.

- **Error Handling**  
  Safely handles failures in downloading or processing and logs problematic links.

## main.py – Logo hashing, similarity grouping
The `main.py` script is responsible for processing all extracted logo images, computing perceptual hashes, calculating extraction success rates, and grouping websites based on visual similarity.

Its main responsibilities include:

- **Hash Loading & Validation**  
  The script loads all perceptual hashes generated during the extraction stage and validates each entry in `good_links.csv`.  

- **Similarity Comparison & Grouping**  
  Every logo hash is compared with all others using the perceptual hash distance (Hamming distance).  
  If two hashes differ by less than the chosen threshold (`THRESHOLD`), they are considered visually similar and included in the same group.

- **Group Export**  
  The output is written to `grouped_links.csv`

## logo_image_group.py 
The `logo_image_group.py` script takes the grouped results and organizes the corresponding images into folders so that visually similar logos can be inspected easily.



