import pandas as pd
df = pd.read_json('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523.json')
df.to_csv('/Users/dana.rocha/Documents/Github/cirro_datasets/test-may15/cirro_datasets_test_150523_formatted_out.csv', index = None)


