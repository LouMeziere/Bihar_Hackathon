import pandas as pd
import re
import csv

# Function to format phone numbers as Indian numbers
def format_indian_phone(number):
    digits = re.sub(r'\D', '', str(number))
    if len(digits) == 10:
        return f"+91 {digits[:5]} {digits[5:]}"
    elif len(digits) == 11 and digits.startswith('0'):
        digits = digits[1:]
        return f"+91 {digits[:5]} {digits[5:]}"
    elif len(digits) > 10:
        return f"+91 {digits[:-10]} {digits[-10:-5]} {digits[-5:]}"
    else:
        return f"+91 {digits}"

# Load CSV file
df = pd.read_csv('datasets/ashrams.csv')

# Format phone numbers
df['phone'] = df['phone'].apply(format_indian_phone)

# Save the updated DataFrame back to CSV (overwrite or new file)
df.to_csv('datasets/ashrams_formatted.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
