import csv
import os
import requests

BAD = "bad_links.csv"
ERROR = "error_links.csv"
TIMEOUT = 15 

def append_csv(filename, row):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def check_site_errors():
    if not os.path.exists(BAD):
        print(f"{BAD} nu există.")
        return

    with open(BAD, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    for row in reader:
        url = row[0]
        print(f"Verificare: {url}")
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
        except Exception as e:
            append_csv(ERROR, [url, str(e)])
            print(f"Eroare la site: {e}")

            remaining = [r for r in reader if r[0] != url]
            with open(BAD, "w", newline="", encoding="utf-8") as f_bad:
                writer = csv.writer(f_bad)
                writer.writerows(remaining)

            reader = remaining

check_site_errors()
