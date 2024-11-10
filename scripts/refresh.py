import csv
import json
import os
import requests
import subprocess
import zipfile


repo_root = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, text=True).stdout.strip()
data_path = os.path.join(repo_root, "data")
compressed_data_file_path = os.path.join(data_path, "US.zip")
extracted_data_path = os.path.join(data_path, "US")
data_file_path = os.path.join(extracted_data_path, "US.txt")
transformed_data_file_name = os.path.join(data_path, "US-condensed.json")
mapped_data_file_name = os.path.join(data_path, "US-condensed-mapped.json")


# Refresh by pulling from Geonames
compressed_data = requests.get(
    "https://download.geonames.org/export/zip/US.zip")

with open(compressed_data_file_path, "wb+") as f:
    f.write(compressed_data.content)

with zipfile.ZipFile(compressed_data_file_path, 'r') as zf:
    zf.extractall(extracted_data_path)

# Transform
data = []
data_as_map = {}
with open(data_file_path, 'r') as tsv_f:
    tsv_reader = csv.reader(tsv_f, delimiter="\t")
    for row in tsv_reader:
        postal_code_info = {
            # "countryCode": row[0],
            "postalCode": row[1],
            "city": row[2],
            # "adminName1": row[3],
            "state": row[4],
            # "adminName2": row[5],
            # "adminCode2": row[6],
            # "adminName3": row[7],
            # "adminCode3": row[8],
            "latitude": float(row[9]),
            "longitude": float(row[10]),
            # "accuracy": row[11],
        }
        data.append(postal_code_info)

        postal_code_info_as_map_value = {
            # "countryCode": row[0],
            # "postalCode": row[1],
            "city": row[2],
            # "adminName1": row[3],
            "state": row[4],
            # "adminName2": row[5],
            # "adminCode2": row[6],
            # "adminName3": row[7],
            # "adminCode3": row[8],
            "latitude": float(row[9]),
            "longitude": float(row[10]),
            # "accuracy": row[11],
        }
        data_as_map[row[1]] = postal_code_info_as_map_value

with open(transformed_data_file_name, 'w') as f:
    json.dump(data, f, indent=2)

with open(mapped_data_file_name, "w") as f:
    json.dump(data_as_map, f, indent=2)
