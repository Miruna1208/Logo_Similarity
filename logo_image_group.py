import os
import shutil
import csv

CSV_FILE = "grouped_links.csv"  
IMAGES_FOLDER = "logos"                
OUTPUT_FOLDER = "grouped_logos"        
UNIQUE_FOLDER = os.path.join(OUTPUT_FOLDER, "Unique_Groups")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(UNIQUE_FOLDER, exist_ok=True)

def url_to_filename(url):
    fname = url.replace("https://", "").rstrip("/") + ".png"
    return fname

groups = []
current_group = []

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if not row or not row[0].strip():
            continue
        val = row[0].strip()
        if val.lower().startswith("group"):
            if current_group:
                groups.append(current_group)
            current_group = []
        else:
            current_group.append(val)
    if current_group:
        groups.append(current_group)

for idx, group in enumerate(groups, 1):
    if len(group) == 1:
        url = group[0]
        src_file = os.path.join(IMAGES_FOLDER, url_to_filename(url))
        if os.path.exists(src_file):
            shutil.copy2(src_file, UNIQUE_FOLDER)
    else:
        folder_name = os.path.join(OUTPUT_FOLDER, f"Group_{idx}")
        os.makedirs(folder_name, exist_ok=True)
        for url in group:
            src_file = os.path.join(IMAGES_FOLDER, url_to_filename(url))
            if os.path.exists(src_file):
                shutil.copy2(src_file, folder_name)
