import json
import csv
import re

# TODO: convert to classes, add main to call classes/methods, user arguments (argparse)

# Read in JSON file
with open("/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523.json", "r") as jsonfile:
    data = jsonfile.read()

# Parse file
json_obj = json.loads(data)

empty_values = ["", [''], [], "[]"]
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

# Fill in missing columns with NA
for index, row in enumerate(json_obj):
    for header in headers:
        if header not in row.keys():
            row[header] = "NA"

for index, data_row in enumerate(json_obj):
    for key, val in data_row.items():
        if isinstance(val, str):
            # Removes non-alphanumeric characters besides whitespace
            new_val = re.sub(r'[^A-Za-z0-9 ]+', '', val)
            data_row[key] = new_val
        # Unlist values of list type
        elif isinstance(val, list) and val not in empty_values:
            val = (",".join(str(item) for item in val))
            data_row[key] = val

# Write out CSV file
with open("test_outfile_all_3.csv", "w", encoding="UTF8", newline="") as fileout:
    writer = csv.DictWriter(fileout, fieldnames=headers)
    writer.writeheader()
    writer.writerows(json_obj)
