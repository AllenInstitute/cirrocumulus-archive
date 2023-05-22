The code presented here takes in a JSON file from MongoDB, cleans the JSON objects, and writes it out to a CSV file. The CSV file will be written to the same directory containing the JSON file. The default output filename is 'cirro_datasets.csv'.

### Usage

```
python3 json_to_csv.py --input ${out_folder}
```

or 

```
python3 json_to_csv.py -i ${out_folder}
```