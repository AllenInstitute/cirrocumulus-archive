import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

class CirroJsonToCSV:
    """ Class to clean the JSON export from MongoDB and write to CSV file"""

    def __init__(self, json_path) -> None:
        """ Initialize class """

        self.json_path = json_path[1]
        self.configs = self._parse_arguments(json_path)
        self.headers = []
        self.empty_values = ["", [''], [], "[]"]
        self.json_to_parse = None
        self.output_filepath = None
    
    def _parse_arguments(self, args: list) -> argparse.Namespace:
        """ Parses sys arguments with argparse """

        error_message = "Input directory must be specified."

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-i",
            "--input",
            required=True,
            help=error_message
        )

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
        
        DEFAULT_JSON_FILENAME = "cirro_datasets.json"
        path_to_check = Path(self.json_path) / DEFAULT_JSON_FILENAME

        assert os.path.isfile(path_to_check), f"The JSON file '{DEFAULT_JSON_FILENAME}' does not exist in this file path '{self.json_path}'."

        if os.path.isfile(path_to_check):
            self.output_filepath = Path(self.json_path)

            with path_to_check.open("r") as jsonfile:
                self.json_to_parse = json.loads(jsonfile.read())

    def fill_empty_values(self):
        """
        Adds "NA" where there are missing values or an empty list in self.json_to_parse,
        Adds headers as strings to self.headers

        Parameters
        ----------
        self

        Returns
        -------
        self.json_to_parse -> list of dictionaries
        """

        for row in self.json_to_parse:
            for key, val in row.items():

                if key not in self.headers:
                    self.headers.append(key)

                # Loop through rows, add NA if value is empty or an empty list
                if val in self.empty_values:
                    row[key] = "NA"

        return self.json_to_parse

    def fill_missing_row_values(self):
        """
        Adds "NA" where there are missing rows in self.json_to_parse,
        # For when JSON object (dictionary) has incorrect number of keys 
        (when a row in the dataset is missing a column)

        Parameters
        ----------
        self

        Returns
        -------
        self.json_to_parse -> list of dictionaries
        """

        for row in self.json_to_parse:
            for header in self.headers:
                if header not in row.keys():
                    row[header] = "NA"

        return self.json_to_parse
    
    def remove_nonalpha_chars_species_col(self):
        """
        Removes non-alphanumeric characters in the Species column
        
        Parameters
        ----------
        self

        Returns
        -------
        self.json_to_parse -> list of dictionaries
        """

        for data_row in self.json_to_parse:
            for key, val in data_row.items():
                if isinstance(val, str) and key == "species":
                    # Removes non-alphanumeric characters besides whitespace
                    new_val = re.sub(r'[^A-Za-z0-9 ]+', '', val)
                    data_row[key] = new_val

        return self.json_to_parse

    def flatten_nested_values(self):
        """
        Flattens values that are nested data structures 
        
        Parameters
        ----------
        self

        Returns
        -------
        self.json_to_parse -> list of dictionaries
        """

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
        """ Writes to CSV file """

        csv_file_path= (self.output_filepath / "cirro_datasets").with_suffix(".csv")

        with csv_file_path.open("w") as fileout:
            writer = csv.DictWriter(fileout, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.json_to_parse)

if __name__ == "__main__":
    sys_args = sys.argv[1:]
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