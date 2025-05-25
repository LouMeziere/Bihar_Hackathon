import snowflake.connector
import toml

import pandas as pd

# Load the CSV file
df = pd.read_csv('cultural_sites.csv')

# Drop the last row
df = df.iloc[:-1]

# Save the updated CSV back, overwriting the original file
df.to_csv('cultural_sites.csv', index=False)