import csv
import os
import imagehash
from PIL import Image

from find_logo_scripts.find_logo import take_logo  

BAD = "bad_links.csv"
GOOD = "good_links.csv"
ERROR = "error_links.csv"

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)

def save_csv(filename, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def process_bad_links():
    bad_rows = load_csv(BAD)
    good_rows = load_csv(GOOD)
    error_rows = load_csv(ERROR)

    new_bad = []

    for row in bad_rows:
        url = row[0]
        print(f"Procesare: {url}")

        try:
            img_path = take_logo(url)
        except Exception as e:
            error_rows.append([url, str(e)])
            print(f"Eroare la deschiderea site-ului: {e}")
            continue 

        if img_path:
            try:
                img = Image.open(img_path)
                h = str(imagehash.average_hash(img))
                good_rows.append([url, h])
                print("Logo found")
            except Exception as e:
                error_rows.append([url, f"Image processing error: {e}"])
                print(f"Eroare la procesarea imaginii: {e}")
        else:
            new_bad.append(row)
            print("Logo not found")

    save_csv(GOOD, good_rows)
    save_csv(BAD, new_bad)
    save_csv(ERROR, error_rows)

process_bad_links()
