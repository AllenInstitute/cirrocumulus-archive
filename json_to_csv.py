import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

# TODO: user arguments (argparse)

class CirroJsonToCSV:
    """ Class to clean the JSON export from MongoDB and write to CSV file"""

    # DEFAULT_FILE_PATH = os.getcwd()
    # DEFAULT_JSON_FILENAME = "example_dataset.json"

    def __init__(self, json_path) -> None:
        self.json_path = json_path[1]
        self.configs = self._parse_arguments(json_path)
        self.headers = []
        self.empty_values = ["", [''], [], "[]"]
        self.json_to_parse = None
        self.output_filepath = None
    
    def _parse_arguments(self, args: list) -> argparse.Namespace:
        
        error_message = "Input directory must be specified."
        # help_message = "Output directory, defaults to current working directory"

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-i",
            "--input",
            required=True,
            help=error_message
        )

        # parser.add_argument(
        #     "-o",
        #     "--output",
        #     required=False,
        #     default=self.DEFAULT_FILE_PATH,
        #     help=help_message,
        # )

        args = parser.parse_args()
        return args

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
        DEFAULT_JSON_FILENAME = "example_dataset.json"
        path_to_check = Path(self.json_path) / DEFAULT_JSON_FILENAME

        # assert os.path.exists(self.json_path), f"The file path '{self.json_path}' does not exist."
        # print(type(self.json_path)) ## string type
        assert os.path.isfile(path_to_check), f"The JSON file '{DEFAULT_JSON_FILENAME}' does not exist in this file path '{self.json_path}'."
        # print(path_to_check)

        if os.path.isfile(path_to_check):
            # print("YES")
            self.output_filepath = Path(self.json_path)

            with path_to_check.open("r") as jsonfile:
                # print("self.json_path:", self.json_path)
                # print(type(self.json_path))
                # print("path_to_check:", path_to_check.parent)
                # print(type(path_to_check.parent))
                # content = jsonfile.read()
                # self.json_to_parse = json.load(content)
                self.json_to_parse = json.loads(jsonfile.read())
        # print(content)
        # print(type(content))
        # print(self.json_to_parse)
        # print(type(self.json_to_parse))
        # print("output_filepath", self.output_filepath)
        # print(type(self.output_filepath))

    def fill_empty_values(self):
        # Add "NA" where there are empty values
        for row in self.json_to_parse:
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
        for row in self.json_to_parse:
            for header in self.headers:
                if header not in row.keys():
                    row[header] = "NA"

        return self.json_to_parse
    
    def remove_nonalpha_chars_species_col(self):
        for data_row in self.json_to_parse:
            for key, val in data_row.items():
                if isinstance(val, str) and key == "species":
                    # Removes non-alphanumeric characters besides whitespace
                    new_val = re.sub(r'[^A-Za-z0-9 ]+', '', val)
                    data_row[key] = new_val

        return self.json_to_parse

    def flatten_nested_values(self):
        unpack_keys = ["_id", "last_updated"]

        for data_row in self.json_to_parse:
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
        # print(type(self.output_filepath))
        csv_file_path= (self.output_filepath / "cirro_datasets_test").with_suffix(".csv")

        with csv_file_path.open("w") as fileout:
            writer = csv.DictWriter(fileout, fieldnames=self.headers)
            writer.writeheader()
            # print(writer)
            # print(type(fileout))
            writer.writerows(self.json_to_parse)

# def main():
#     initialize = CirroJsonToCSV("example_dataset.json")
#     initialize.load_json()
#     initialize.fill_empty_values()
#     initialize.fill_missing_row_values()
#     initialize.remove_nonalpha_chars_species_col()
#     initialize.flatten_nested_values()
#     initialize.write_to_csv()

if __name__ == "__main__":
    # main()
    sys_args = sys.argv[1:]
    # print(type(sys_args))
    initialize = CirroJsonToCSV(sys_args)
    initialize.load_json()

    if initialize.json_to_parse:
        initialize.fill_empty_values()
        initialize.fill_missing_row_values()
        initialize.remove_nonalpha_chars_species_col()
        initialize.flatten_nested_values()
        initialize.write_to_csv()
    else:
        AssertionError("JSON file is invalid.")