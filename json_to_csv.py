import csv
import json
import os
import re
# from pathlib import Path

# TODO: convert to classes, add main to call classes/methods, user arguments (argparse)
EMPTY_VALUES = ["", [''], [], "[]"]
HEADERS = []

class CirroJsonToCSV:
    """ Class to clean JSON export from MongoDB and write to CSV file"""

    @staticmethod
    def load_json(path: str) -> json:
        """
        Loads JSON from a path
        Parameters
        ----------
        path : str

        Returns
        -------
        json
        """
        assert os.path.exists(path), f"JSON file at '{path}' does not exist."
        if os.path.exists(path):
            with open(path, "r") as jsonfile:
                print("load_json!")
                return json.loads(jsonfile)
                # return jsonfile.read()
    
    def __init__(self) -> None:
        self.json_to_parse = self.load_json()

    def fill_empty_values(self):
        # json_obj = json.loads(json_to_parse)

        # Add "NA" where there are empty values
        for index, row in enumerate(self.json_to_parse):
            for key, val in row.items():

                if key not in HEADERS:
                    HEADERS.append(key)

                # Loop through rows, add NA if value is empty or an empty list
                if val in EMPTY_VALUES:
                    row[key] = "NA"
        return self.json_to_parse

    def write_to_csv(self):
        with open("cirro_datasets.csv", "w", encoding="UTF8", newline="") as fileout:
            writer = csv.DictWriter(fileout, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(self.json_to_parse)


def fill_missing_row_values(file_to_clean):
    # Fill in missing row values with NA
    # Useful for when object has incorrect number of keys (when a row in the dataset is missing a column)
    for index, row in enumerate(file_to_clean):
        for header in HEADERS:
            if header not in row.keys():
                row[header] = "NA"

    return file_to_clean

def remove_nonalpha_chars_species_col(in_file):
    for index, data_row in enumerate(in_file):
        for key, val in data_row.items():
            if isinstance(val, str) and key == "species":
                # Removes non-alphanumeric characters besides whitespace
                new_val = re.sub(r'[^A-Za-z0-9 ]+', '', val)
                data_row[key] = new_val

    return in_file

def flatten_nested_values(json_file_to_parse):
    unpack_keys = ["_id", "last_updated"]

    for index, data_row in enumerate(json_file_to_parse):
        for key, val in data_row.items():
            # Unnest "oid" and "date" values from dictionary
            if key in unpack_keys:
                for nested_key, nested_val in val.items():
                    data_row[key] = nested_val
            # Unlist values of list type (e.g. ["10x multiome", "Smart-seq"] to "10x multiome,Smart-seq")
            elif isinstance(val, list) and val not in EMPTY_VALUES:
                val = (",".join(str(item) for item in val))
                data_row[key] = val

    return json_file_to_parse

def write_to_csv(file_to_write):
    with open("cirro_datasets.csv", "w", encoding="UTF8", newline="") as fileout:
        writer = csv.DictWriter(fileout, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(file_to_write)




# def main():
#     loaded_file = load_json("mongo-export/cirro_datasets_test_150523.json")
#     parsed_json = fill_empty_values(loaded_file)
#     flattened_json = flatten_nested_values(parsed_json)
#     filled_missing_rows = fill_missing_row_values(flattened_json)
#     removed_non_alpha = remove_nonalpha_chars_species_col(filled_missing_rows)
#     write_to_csv(removed_non_alpha)

def main():
    convert_json = CirroJsonToCSV.load_json("mongo-export/cirro_datasets_test_150523.json")

if __name__ == "__main__":
    main()
