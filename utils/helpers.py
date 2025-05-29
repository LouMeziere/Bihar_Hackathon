# -------------------------------
#           Imports
# -------------------------------

import streamlit as st
import pandas as pd
import toml
import os
import snowflake.connector
import json
import pydeck as pdk



# Define the order of months for consistent display
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

# GitHub base path once 
GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"


import streamlit as st

def inject_global_css():
    st.markdown("""
        <style>
                
        [data-testid="stSidebar"] {
        width: 250px !important;  /* Change this value as needed */
        }
                
        [data-testid="stSidebar"] > div:first-child {
            width: 250px !important;
        }
                
        .container {
            max-width: 850px ;
            margin: 0 auto ;
            padding: 24px ;
            text-align: left;
        }

        h2, .subtitle {
            color: #ffffff; 
            font-weight: 900; 
            font-size: 44px; 
            max-width: 850px;
            margin: 0 auto;
            text-align: left;
        }

        p {
            color: #93aca4;  
            font-size: 1.2rem;   
        }    

        </style>
    """, unsafe_allow_html=True)

"""
def connect_to_snowflake():
    conn_info = {
        "account": st.secrets["snowflake"]["account"],
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "role": st.secrets["snowflake"]["role"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"],
    }
    return snowflake.connector.connect(**conn_info)

"""
def connect_to_snowflake():
    # Read Snowflake connection credentials from environment variables
    conn_info = {
        'account': os.getenv('ACCOUNT'),
        'user': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
        'role': os.getenv('ROLE'),            # optional but you had it in toml
        'warehouse': os.getenv('WAREHOUSE'),
        'database': os.getenv('DATABASE'),
        'schema': os.getenv('SCHEMA')
    }
    
    # Connect using the dictionary of connection parameters
    return snowflake.connector.connect(**conn_info)




def load_table(table_name: str, schema: str = "discover_india.public") -> pd.DataFrame:
    """
    Load a table from Snowflake and convert column names to lowercase.

    Parameters:
    - table_name (str): The name of the table to load.
    - schema (str): The schema where the table is located (default: discover_india.public).

    Returns:
    - pd.DataFrame: The resulting DataFrame with lowercase column names.
    """
    conn = connect_to_snowflake()  # Establish connection
    query = f'SELECT * FROM {schema}.{table_name}'  # Prepare SQL query
    df = pd.read_sql(query, conn)  # Execute query and load data into DataFrame
    conn.close()  # Close connection
    df.columns = [col.lower() for col in df.columns]  # Normalize column names to lowercase
    return df


@st.cache_data
def load_all_data():
    # Load all relevant data tables from Snowflake and cache for efficiency
    df_site = load_table("cultural_sites")
    df_festival = load_table("festivals_data")
    df_art = load_table("arts")
    df_weather = load_table("weather_data")
    return df_site, df_festival, df_art, df_weather


def render_sidebar():
    # Load all data needed for filtering options
    df_culture, df_festival, df_art, df_weather = load_all_data()

    # Combine unique states from all datasets for selection options
    states = pd.concat([
        df_culture['state'], 
        df_festival['state'], 
        df_art['state'], 
        df_weather['state']
    ]).dropna().unique()

    with st.sidebar:
        st.markdown(
            '<h2 style="text-align: left;">Customize Your Exploration</h2>',
            unsafe_allow_html=True
        )

        selected_states = st.multiselect(
            "🗺️ Select State(s):", 
            sorted(states),
            default=st.session_state.get("state_selector", []),
            key="state_selector"
        )

        selected_months = st.multiselect(
            "📅 Select Month(s):",
            month_order,
            default=st.session_state.get("month_selector", []),
            key="month_selector"
        )

    # Just return the values—no need to set them manually
    return selected_states, selected_months



@st.cache_data
def load_geojson(path):
    with open(path, "r") as f:
        return json.load(f)

def create_map():
    lines_data = load_geojson("images/railway/railways_lines_cleaned.geojson")
    points_data = load_geojson("images/railway/railways_points_cleaned.geojson")

    rail_layer = pdk.Layer(
        "GeoJsonLayer",
        lines_data,
        get_line_color=[255, 0, 0],
        get_line_width=2,
        pickable=True
    )

    points_layer = pdk.Layer(
        "GeoJsonLayer",
        points_data,
        get_fill_color=[52, 244, 164, 160],
        get_radius=1000,
        point_radius_min_pixels=2,
        point_radius_max_pixels=10,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=22.9734,
        longitude=78.6569,
        zoom=4,
        pitch=0
    )

    return pdk.Deck(
        layers=[rail_layer, points_layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"}
    )

