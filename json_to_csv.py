import pandas as pd
import json
import csv

# class to read in json
# write out CSV file

# df = pd.read_json('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523.json')
# df.to_csv('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523_formatted_out.csv', index = None)

f = open('example_dataset.json', 'r')

data = json.loads(f.read())

empty_values = ["", [''], []]
unpack_keys = ["_id", "last_updated"]

for index, row in enumerate(data):
    for key, val in row.items():
        if val in empty_values:
            row[key] = "NA"
        if key in "_id" or key == "last_updated":
            for nested_key, nested_val in val.items():
                row[key] = nested_val
f.close()

fileout = open("/Users/dana.rocha/Documents/Github/cirro_datasets/out.csv", "w")
writer = csv.writer(fileout)
writer.writerow(data)
fileout.close()
# class to clean dataset
# loop through columns, add NA if value is empty

# class to call, user arguments (argparse)