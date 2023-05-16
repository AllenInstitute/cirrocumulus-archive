import json
import csv

# class to read in json

# Read file
with open("example_dataset.json", "r") as jsonfile:
    data = jsonfile.read()

# Parse file
json_obj = json.loads(data)

empty_values = ["", [''], []]
unpack_keys = ["_id", "last_updated"]

headers = []

# Clean dataset
for index, row in enumerate(json_obj):
    for key, val in row.items():
        if key not in headers:
            headers.append(key)
        # loop through rows, add NA if value is empty or empty list
        if val in empty_values:
            row[key] = "NA"
        if key in "_id" or key == "last_updated":
            for nested_key, nested_val in val.items():
                row[key] = nested_val

# Write out CSV file
with open("formatted_out_3.csv", "w", encoding="UTF8", newline="") as fileout:
    writer = csv.DictWriter(fileout, fieldnames=headers)
    writer.writeheader()
    writer.writerows(json_obj)


# Call, user arguments (argparse)