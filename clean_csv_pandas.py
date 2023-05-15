import pandas as pd

# Read in the CSV file, fill in empty cells with 'NA'
# cirro_data = pd.read_csv("cirro_datasets_first.csv", lineterminator="\n", header=None)
# cirro_data.fillna("NA", inplace=True)
# print(cirro_data.head())

# cirro_data = pd.read_json("cirro_datasets_test_flag.json")
# cirro_data.replace("", "NA", regex=True)
cirro_data = pd.read_csv("cirro_datasets_formatted.csv")
cirro_data.replace("", "NA", regex=True)

for (colname, colval) in cirro_data.iteritems():
    print(colname, colval.values)

# cirro_data.replace(to_replace=r'^\s*$', value="NA", regex=True)
# cirro_data.replace(to_replace="", value="NA", regex=True)


# cirro_data.fillna("NA", inplace=True)
# print(pd.DataFrame(cirro_data))

# replace = [[''], [], ""]

# for col in cirro_data:
    # print(cirro_data[col].values)
    # count = 0

    # for val in cirro_data[col].values:
    #     if val in replace:
    #         val = col.replace(val, "NA")
        # count += 1
        # print("yes")
    # print(count)
    # cirro_data[col].str.replace("{'$oid': '618d86728fc3b606ac4f5da4'}", "NA")
# print(cirro_data["readers"].head())

# {'$oid': '618d86728fc3b606ac4f5da4'} 
cirro_data.to_csv("/Users/dana.rocha/Documents/Github/cirro_datasets_clean_test.csv", index = None)
# count = 0
# for (index, col) in enumerate(cirro_data):
    # print(index, col)
    # print(index, cirro_data[col])
#     for val in cirro_data[col].values:
#         if val in replace:
#             print("YES")
#             count += 1
#         print("no")
# print(count)
# print(cirro_data.info())