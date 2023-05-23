#! /bin/bash

output_dir=/home/dana.rocha/test_cirro_archive
current_date=$(date +"%Y_%m_%d")
mongoexport --db cirrocumulus --collection datasets --jsonArray --out ${output_dir}/${current_date}/cirro_datasets.json
python3 json_to_csv.py --input ${output_dir}/${current_date}