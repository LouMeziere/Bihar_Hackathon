import snowflake.connector
import toml

import pandas as pd

# Load the CSV file
df = pd.read_csv('../datasets/cultural_sites.csv')

# Drop the last row
df = df.iloc[:-1]

# Save the updated CSV back, overwriting the original file
df.to_csv('../datasets/cultural_sites.csv', index=False)
def connect_to_snowflake():
    secrets = toml.load('/Users/loumeziere/Desktop/secret_files/secrets.toml')
    conn_info = secrets['connections']['my_example_connection']
    return snowflake.connector.connect(**conn_info)

# Define your table schemas here (table_name -> list of (col_name, type))
table_schemas = {
    "ashrams": [
        ("name", "STRING"),
        ("state", "STRING"),
        ("phone", "STRING"),
        ("email", "STRING"),
        ("image_url", "STRING"),
        ("description", "STRING"),
    ],
    "arts": [
        ("name", "STRING"),
        ("type", "STRING"),
        ("state", "STRING"),
        ("image_url", "STRING"),
    ],
    "budget_allocation": [
        ("year", "STRING"),
        ("funds_allocated_released_by_ministry_of_culture", "STRING"),
        ("funds_utilised_by_seven_zccs", "STRING"),
    ],
    "co2_emissions_transports": [
        ("mode", "STRING"),
        ("category", "STRING"),
        ("transport_gm_tkm", "STRING"),
    ],
    "cultural_sites": [
        ("monument", "STRING"),
        ("unesco", "STRING"),
        ("latitude", "STRING"),
        ("longitude", "STRING"),
        ("city", "STRING"),
        ("state", "STRING"),
        ("domestic_2022_23", "STRING"),
        ("foreign_2022_23", "STRING"),
        ("total_visitors_2022_23", "STRING"),
        ("domestic_2023_24", "STRING"),
        ("foreign_2023_24", "STRING"),
        ("total_visitors_2023_24", "STRING"),
        ("domestic_growth_percent", "STRING"),
        ("foreign_growth_percent", "STRING"),
        ("image_url", "STRING"),
    ],
    "festivals_data": [
        ("festival_name", "STRING"),
        ("genre", "STRING"),
        ("city", "STRING"),
        ("state", "STRING"),
        ("start_date", "STRING"),
        ("end_date", "STRING"),
        ("description", "STRING"),
    ],
    "monthwise_itas": [
        ("months", "STRING"),
        ("_2021", "STRING"),
        ("_2022", "STRING"),
        ("_2023", "STRING"),
        ("growth_2022_21_percent", "STRING"),
        ("growth_2023_22_percent", "STRING"),
    ],
    "person_benefited_handicraft": [
        ("s_no", "STRING"),
        ("state_uts", "STRING"),
        ("total_no_of_persons_benefitted", "STRING"),
    ],
    "unesco_sites": [
        ("countries", "STRING"),
        ("site_amount", "STRING"),
    ],
    "weather_data": [
        ("city", "STRING"),
        ("state", "STRING"),
        ("month", "STRING"),
        ("avg_temperature_c", "STRING"),
        ("min_temperature_c", "STRING"),
        ("max_temperature_c", "STRING"),
        ("rainfall_mm", "STRING"),
        ("humidity_percent", "STRING"),
        ("rainy_days_d", "STRING"),
        ("avg_sun_hours_hours", "STRING"),
    ],
}

conn = connect_to_snowflake()
cur = conn.cursor()

# Step 1: Create file format (once)
cur.execute("""
    CREATE OR REPLACE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
""")

# Step 2: List files in stage
cur.execute("LIST @datasets_stage")
files = cur.fetchall()

for file in files:
    file_path = file[0]  # e.g. 'datasets_stage/my_file.csv'
    file_name = file_path.split('/')[-1]

    if not file_name.endswith('.csv'):
        continue
    
    table_name = file_name.replace('.csv', '').lower()
    print(f"Creating and loading table: {table_name}")

    if table_name not in table_schemas:
        print(f"Warning: No schema defined for table '{table_name}', skipping.")
        continue
    
    # Step 3: Create table with predefined schema
    columns_def = ", ".join([f"{col} {dtype}" for col, dtype in table_schemas[table_name]])
    create_sql = f"CREATE OR REPLACE TABLE {table_name} ({columns_def});"
    cur.execute(create_sql)

    # Step 4: Load data into table
    copy_sql = f"""
    COPY INTO {table_name}
    FROM @datasets_stage/{file_name}
    FILE_FORMAT = (FORMAT_NAME = 'my_csv_format')
    FORCE = TRUE
    """
    cur.execute(copy_sql)
    copy_result = cur.fetchall()
    print(f"Copy result for {table_name}: {copy_result}")

cur.close()
conn.close()
