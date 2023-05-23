## Overview

The shell commands in `archive_cirro.sh` exports the data stored in the Cirrocumulus MongoDB instance to a JSON file in a directory named with the export date. Then `json_to_csv.py` is used to write that JSON file to a CSV file.

The code presented in `json_to_csv.py` takes in a JSON file from MongoDB, cleans the JSON objects, and writes it out to a CSV file. The CSV file will be written to the same directory containing the JSON file. The default output filename is 'cirro_datasets.csv'.

### Usage (json_to_csv.py)

```
python3 json_to_csv.py --input ${out_folder}
```

or 

```
python3 json_to_csv.py -i ${out_folder}
```