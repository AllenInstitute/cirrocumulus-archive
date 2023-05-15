import pandas as pd

# class to read in json and write out CSV file
df = pd.read_json('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523.json')
df.to_csv('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523_formatted_out.csv', index = None)

# class to clean dataset
# loop through columns, add NA if value is empty

# class to call, user arguments (argparse)
