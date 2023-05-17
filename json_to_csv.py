import json
import csv
import re
import sys

# TODO: convert to classes, add main to call classes/methods, user arguments (argparse)
EMPTY_VALUES = ["", [''], [], "[]"]
HEADERS = []

def load_json(path):
    with open(path, "r") as jsonfile:
        # print("yes")
        return jsonfile.read()

def fill_empty_values(json_to_parse):
    json_obj = json.loads(json_to_parse)

    # empty_values = ["", [''], [], "[]"]
    # unpack_keys = ["_id", "last_updated"]

    # Add "NA" where there are empty values
    for index, row in enumerate(json_obj):
        for key, val in row.items():

            if key not in HEADERS:
                HEADERS.append(key)

            # Loop through rows, add NA if value is empty or empty list
            if val in EMPTY_VALUES:
                row[key] = "NA"

            # if key in unpack_keys:
                # Unnest "oid" and "date" values from dictionary
                # for nested_key, nested_val in val.items():
                    # row[key] = nested_val
    return json_obj

def fill_missing_row_values(file_to_clean):
    # Fill in missing row values with NA
    for index, row in enumerate(file_to_clean):
        for header in HEADERS:
            if header not in row.keys():
                row[header] = "NA"
    return file_to_clean

# def remove_nonalpha_chars(in_file):
#     for index, data_row in enumerate(in_file):
#         for key, val in data_row.items():
#             if isinstance(val, str):
#                 # Removes non-alphanumeric characters besides whitespace
#                 new_val = re.sub(r'[^A-Za-z0-9 ]+', '', val)
#                 data_row[key] = new_val
#             # Unlist values of list type
#             elif isinstance(val, list) and val not in EMPTY_VALUES:
#                 val = (",".join(str(item) for item in val))
#                 data_row[key] = val
#         return in_file

def flatten_nested_values(json_file_to_parse):
    # empty_values = ["", [''], [], "[]"]
    unpack_keys = ["_id", "last_updated"]

    # Dont uncomment
    # for index, row in enumerate(json_obj):
    #     for key, val in row.items():

    #         if key in unpack_keys:
    #             # Unnest "oid" and "date" values from dictionary
    #             for nested_key, nested_val in val.items():
    #                 row[key] = nested_val


    for index, data_row in enumerate(json_file_to_parse):
        for key, val in data_row.items():
            # Unnest "oid" and "date" values from dictionary
            if key in unpack_keys:
                for nested_key, nested_val in val.items():
                    data_row[key] = nested_val
            # Unlist values of list type
            elif isinstance(val, list) and val not in EMPTY_VALUES:
                val = (",".join(str(item) for item in val))
                data_row[key] = val
    return json_file_to_parse



def main():
    loaded_file = load_json("example_dataset.json")
    parsed_json = fill_empty_values(loaded_file)
    flattened_json = flatten_nested_values(parsed_json)
    filled_missing_rows = fill_missing_row_values(flattened_json)
    print(filled_missing_rows)
    # print("made it here")
    # print(HEADERS)

# # Write out CSV file
# with open("test_outfile_all_3.csv", "w", encoding="UTF8", newline="") as fileout:
#     writer = csv.DictWriter(fileout, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(json_obj)

if __name__ == "__main__":
    main()
