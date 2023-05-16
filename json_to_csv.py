import json
import csv

# Read in JSON file
with open("/Users/dana.rocha/Documents/Github/cirro_datasets/example_dataset.json", "r") as jsonfile:
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

# Unlist values of list type
for index, row in enumerate(json_obj):
    for key, val in row.items():
        if isinstance(val, list) and val not in empty_values:
            # for i in range(len(val) - 1, 0, -1):
            #     val = val.pop)_
            val = (",".join(str(item) for item in val))
            row[key] = val


# # Write out CSV file
with open("formatted_out_9.csv", "w", encoding="UTF8", newline="") as fileout:
    writer = csv.DictWriter(fileout, fieldnames=headers)
    writer.writeheader()
    writer.writerows(json_obj)

# Call, user arguments (argparse)