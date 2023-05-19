import csv
import json
import os
import re

# TODO: convert to classes, add main to call classes/methods, user arguments (argparse)

# EMPTY_VALUES = ["", [''], [], "[]"]
# HEADERS = []

class CirroJsonToCSV:
    """ Class to clean the JSON export from MongoDB and write to CSV file"""

    def __init__(self, json_path) -> None:
        self.json_path = json_path
        self.json_to_parse = None
        self.headers = []
        self.empty_values = ["", [''], [], "[]"]

    def load_json(self):
        """
        Loads JSON from a path
        Parameters
        ----------
        path : str

        Returns
        -------
        json
        """
        assert os.path.exists(self.json_path), f"JSON file at '{self.json_path}' does not exist."
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as jsonfile:
                self.json_to_parse = json.load(jsonfile)
    
    def fill_empty_values(self):
        # Add "NA" where there are empty values
        for index, row in enumerate(self.json_to_parse):
            for key, val in row.items():

                if key not in self.headers:
                    self.headers.append(key)

                # Loop through rows, add NA if value is empty or an empty list
                if val in self.empty_values:
                    row[key] = "NA"

        return self.json_to_parse

    def fill_missing_row_values(self):
        # Fill in missing row values with NA
        # For when JSON object (dictionary) has incorrect number of keys (when a row in the dataset is missing a column)
        for index, row in enumerate(self.json_to_parse):
            for header in self.headers:
                if header not in row.keys():
                    row[header] = "NA"

        return self.json_to_parse
    
    def remove_nonalpha_chars_species_col(self):
        for index, data_row in enumerate(self.json_to_parse):
            for key, val in data_row.items():
                if isinstance(val, str) and key == "species":
                    # Removes non-alphanumeric characters besides whitespace
                    new_val = re.sub(r'[^A-Za-z0-9 ]+', '', val)
                    data_row[key] = new_val

        return self.json_to_parse

    def flatten_nested_values(self):
        unpack_keys = ["_id", "last_updated"]

        for index, data_row in enumerate(self.json_to_parse):
            for key, val in data_row.items():
                # Unnest "oid" and "date" values from dictionary
                if key in unpack_keys:
                    for nested_key, nested_val in val.items():
                        data_row[key] = nested_val
                # Unlist values of list type (e.g. ["10x multiome", "Smart-seq"] to "10x multiome,Smart-seq")
                elif isinstance(val, list) and val not in self.empty_values:
                    val = (",".join(str(item) for item in val))
                    data_row[key] = val

        return self.json_to_parse

    def write_to_csv(self):
        with open("cirro_datasets.csv", "w", encoding="UTF8", newline="") as fileout:
            writer = csv.DictWriter(fileout, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.json_to_parse)

def main():
    initialize = CirroJsonToCSV("example_dataset.json")
    initialize.load_json()
    initialize.fill_empty_values()
    initialize.fill_missing_row_values()
    initialize.remove_nonalpha_chars_species_col()
    initialize.flatten_nested_values()
    initialize.write_to_csv()

if __name__ == "__main__":
    main()
