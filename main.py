import pyarrow.parquet as pq
import csv
from PIL import Image
import imagehash

data = pq.read_table("C:/Users/Miruna/Documents/Job/Logo_Similarity/logos.snappy.parquet")

good_rows = []
with open('csv_files/good_links.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)  
    for row in reader:
        good_rows.append(row)

error_rows = []
with open('csv_files/error_links.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)  
    for row in reader:
        error_rows.append(row)

good_links = len(good_rows)
error_links = len(error_rows)
total_links = data.num_rows
success_rate = (good_links / (total_links - error_links)) * 100

print("Success rate:", success_rate)

GOOD = "csv_files/good_links.csv"
GROUPED = "grouped_links.csv"
THRESHOLD = 18

links_hashes = []
with open(GOOD, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        url = row[0]
        hash_str = row[1]
        try:
            h = imagehash.hex_to_hash(hash_str)
            links_hashes.append((url, h))
        except ValueError:
            continue

groups = []
used = set()

for i, (url1, h1) in enumerate(links_hashes):
    if i in used:
        continue
    group = [url1]
    used.add(i)
    for j, (url2, h2) in enumerate(links_hashes):
        if j in used:
            continue
        if h1 - h2 <= THRESHOLD:
            group.append(url2)
            used.add(j)
    groups.append(group)

with open(GROUPED, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for idx, group in enumerate(groups, 1):
        writer.writerow([f"Group {idx}"])
        for url in group:
            writer.writerow([url])
        writer.writerow([])  

print(f"{len(groups)} grupuri salvate în {GROUPED}")

