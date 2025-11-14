import csv
import find_logo_scripts.find_logo as find_logo
import pyarrow.parquet as pq
from PIL import Image
import imagehash

data = pq.read_table('C:/Users/Miruna/Documents/Logo_similarity/logos.snappy.parquet')
good_links_file = 'good_links.csv'
bad_links_file = 'bad_links.csv'

with open(good_links_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['link', 'hash'])
    writer.writeheader()

with open(bad_links_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['link', 'error'])
    writer.writeheader()

good_count = 0
total_links = len(data[0])


for i in range(total_links):
    domain = str(data[0][i])
    url = f"https://www.{domain}"
    try:
        logo_path = find_logo.take_logo(url)
        if logo_path:
            try:
                img = Image.open(logo_path)
                img_hash = str(imagehash.phash(img))
            except Exception:
                img_hash = ''
            with open(good_links_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['link', 'hash'])
                writer.writerow({'link': url, 'hash': img_hash})
            good_count += 1
        else:
            with open(bad_links_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['link', 'error'])
                writer.writerow({'link': url, 'error': 'logo not found'})
    except Exception as e:
        with open(bad_links_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['link', 'error'])
            writer.writerow({'link': url, 'error': str(e)})
