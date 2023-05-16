import pandas as pd
import json
import csv

# class to read in json
# write out CSV file

# df = pd.read_json('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523.json')
# df.to_csv('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523_formatted_out.csv', index = None)

# Read file
with open("example_dataset.json", "r") as jsonfile:
    data = jsonfile.read()

# Parse file
json_obj = json.loads(data)

empty_values = ["", [''], []]
unpack_keys = ["_id", "last_updated"]

headers = []

for index, row in enumerate(json_obj):
    for key, val in row.items():
        if key not in headers:
            headers.append(key)
        if val in empty_values:
            row[key] = "NA"
        if key in "_id" or key == "last_updated":
            for nested_key, nested_val in val.items():
                row[key] = nested_val

with open("formatted_out_2.csv", "w", encoding="UTF8", newline="") as fileout:
    writer = csv.DictWriter(fileout, fieldnames=headers)
    # writer.writerow(headers)
    writer.writerows(json_obj)

# class to clean dataset
# loop through columns, add NA if value is empty

# class to call, user arguments (argparse)