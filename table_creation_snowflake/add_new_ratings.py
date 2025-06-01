# ion_snowflake/add_new_ratings.py

import pandas as pd
from utils.helpers import connect_to_snowflake

FEEDBACK_FILE = "datasets/feedback_data.csv"

table_schemas = {
    "feedback_data": [
        ("name", "STRING"),
        ("feedback", "STRING"),
        ("rating", "INT"),
    ],
}

def upload_feedback_to_snowflake():
    # Connect to Snowflake
    conn = connect_to_snowflake()
    cursor = conn.cursor()

    # Read the CSV file
    df = pd.read_csv(FEEDBACK_FILE)

    # Create table if not exists
    schema = table_schemas["feedback_data"]
    columns_sql = ", ".join([f"{col} {dtype}" for col, dtype in schema])
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS feedback_data (
            {columns_sql}
        )
    """
    cursor.execute(create_table_sql)

    # Optional: Clear the table before inserting fresh data, or do UPSERT logic
    cursor.execute("TRUNCATE TABLE feedback_data")

    # Insert data (batch insert for efficiency)
    insert_sql = "INSERT INTO feedback_data (name, feedback, rating) VALUES (%s, %s, %s)"
    data_to_insert = [tuple(x) for x in df.to_numpy()]
    cursor.executemany(insert_sql, data_to_insert)
    conn.commit()

    cursor.close()
    conn.close()



def upload_feedback_to_snowflake_param(name: str, feedback: str, rating: int):
    # Connect to Snowflake
    conn = connect_to_snowflake()
    cursor = conn.cursor()

    # Ensure the table exists
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS feedback_data (
            name STRING,
            feedback STRING,
            rating INT
        )
    """
    cursor.execute(create_table_sql)

    # Insert a single new record (avoid truncating)
    insert_sql = "INSERT INTO feedback_data (name, feedback, rating) VALUES (%s, %s, %s)"
    cursor.execute(insert_sql, (name, feedback, rating))

    conn.commit()
    cursor.close()
    conn.close()
