import pandas as pd

# dictionary of lists
dictionary = {'name':["aparna", "pankaj", "sudhir", "Geeku"],
        'degree': ["MBA", "BCA", "M.Tech", "MBA"],
        'score':[90, 40, 80, 98]}

# Creating a dataframe from a dictionary
df = pd.DataFrame(dictionary)

# Using items() function to retrieve rows
# The iteritems() function was deprecated
for key, value in df.items():
    print(key, value)
    print("---")