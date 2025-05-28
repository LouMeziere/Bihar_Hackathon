
# -------------------------------
#           Imports
# -------------------------------

import pandas as pd
from utils.helpers import connect_to_snowflake


# -------------------------------
#       Assign column names
# -------------------------------

# Define your table schemas here (table_name -> list of (col_name, type))
table_schemas = {
    "ashrams_formatted": [
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
        ("year", "NUMBER"),
        ("funds_allocated_released_by_ministry_of_culture", "NUMBER"),
        ("funds_utilised_by_seven_zccs", "NUMBER"),
    ],
    "co2_emissions_transports": [
        ("mode", "STRING"),
        ("category", "STRING"),
        ("transport_gm_tkm", "NUMBER"),
    ],
    "cultural_sites": [
        ("monument", "STRING"),
        ("unesco", "BOOLEAN"),
        ("latitude", "FLOAT"),
        ("longitude", "FLOAT"),
        ("city", "STRING"),
        ("state", "STRING"),
        ("domestic_2022_23", "NUMBER"),
        ("foreign_2022_23", "NUMBER"),
        ("total_visitors_2022_23", "NUMBER"),
        ("domestic_2023_24", "NUMBER"),
        ("foreign_2023_24", "NUMBER"),
        ("total_visitors_2023_24", "NUMBER"),
        ("domestic_growth_percent", "FLOAT"),
        ("foreign_growth_percent", "FLOAT"),
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
        ("_2021", "NUMBER"),
        ("_2022", "NUMBER"),
        ("_2023", "NUMBER"),
        ("growth_2022_21_percent", "FLOAT"),
        ("growth_2023_22_percent", "FLOAT"),
    ],
    "person_benefited_handicraft": [
        ("s_no", "NUMBER"),
        ("state_uts", "STRING"),
        ("total_no_of_persons_benefitted", "NUMBER"),
    ],
    "unesco_sites_per_country": [
        ("countries", "STRING"),
        ("site_amount", "NUMBER"),
    ],
    "weather_data": [
        ("city", "STRING"),
        ("state", "STRING"),
        ("month", "STRING"),
        ("avg_temperature_c", "FLOAT"),
        ("min_temperature_c", "FLOAT"),
        ("max_temperature_c", "FLOAT"),
        ("rainfall_mm", "FLOAT"),
        ("humidity_percent", "FLOAT"),
        ("rainy_days_d", "NUMBER"),
        ("avg_sun_hours_hours", "FLOAT"),
    ],
}



# -------------------------------
#           Connection
# -------------------------------

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
