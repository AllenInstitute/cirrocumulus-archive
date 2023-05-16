import pandas as pd

data = pd.read_csv("nba.csv")

for index, row in data.iterrows():
    print(index, row)
    print("---")

# print(data.info())