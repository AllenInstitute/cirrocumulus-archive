import pandas as pd

# dictionary of lists
dictionary = {'name':["aparna", "pankaj", "sudhir", "Geeku"],
        'degree': ["MBA", "BCA", "M.Tech", "MBA"],
        'score':[90, 40, 80, 98]}

# Creating a dataframe from a dictionary
df = pd.DataFrame(dictionary)

# Iterating over rows using the iterrows() function
for index, row in df.iterrows():
    print(index, row)
    print("---")