
# main.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image
import streamlit.components.v1 as components
import re
import plotly.express as px
import plotly.graph_objects as go




import toml
import snowflake.connector

# Load secrets.toml
secrets = toml.load('secrets.toml')

# Extract your connection details
conn_info = secrets['connections']['my_example_connection']

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=conn_info['account'],
    user=conn_info['user'],
    password=conn_info['password'],
    role=conn_info['role'],
    warehouse=conn_info['warehouse'],
    database=conn_info['database'],
    schema=conn_info['schema']
)

cursor = conn.cursor()

# Query to check images exist
try:
    cursor.execute("LIST @cultural_images_stage")
    files = cursor.fetchall()
    for f in files:
        print(f)  # Each f contains metadata including filename
except Exception as e:
    print("Error listing files:", e)



cursor.close()
conn.close()


