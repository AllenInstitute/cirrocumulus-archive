import pandas as pd

# Create a sample dataframe
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# Loop through columns using a for loop
for col in df.columns:
    print(col)