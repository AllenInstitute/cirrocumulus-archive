import pandas as pd

# Read in the CSV file, fill in empty cells with 'NA'
cirro_data = pd.read_csv("cirro_datasets_formatted.csv")
cirro_data.fillna("NA", inplace=True)
# print(cirro_data.head())

# Remove unnecessary characters in column values
cirro_data["_id"] = cirro_data["_id"].str.replace("'}","")
cirro_data["_id"] = cirro_data["_id"].str.replace("{'$oid': '","")

cirro_data["species"] = cirro_data["species"].str.replace('["',"")
cirro_data["species"] = cirro_data["species"].str.replace('"]',"")
cirro_data["species"] = cirro_data["species"].str.replace("['","")
cirro_data["species"] = cirro_data["species"].str.replace("']","")
cirro_data["species"] = cirro_data["species"].str.replace("[]","NA")

cirro_data["last_updated"] = cirro_data["last_updated"].str.replace("'}","")
cirro_data["last_updated"] = cirro_data["last_updated"].str.replace("{'$date': '","")

cirro_data["readers"] = cirro_data["readers"].str.replace("['']","NA")
cirro_data["owners"] = cirro_data["owners"].str.replace("['']","NA")

cirro_data["contacts"] = cirro_data["contacts"].str.replace("[]","NA")
cirro_data["library"] = cirro_data["library"].str.replace("[]","NA")
cirro_data["library"] = cirro_data["library"].str.replace("['","")
cirro_data["library"] = cirro_data["library"].str.replace("']","")
cirro_data["library"] = cirro_data["library"].str.replace('["',"")
cirro_data["library"] = cirro_data["library"].str.replace('"]',"")
cirro_data["library"] = cirro_data["library"].str.replace('", "',",")

cirro_data.to_csv("/Users/dana.rocha/Documents/Github/cirro_datasets_clean.csv", index = None)
