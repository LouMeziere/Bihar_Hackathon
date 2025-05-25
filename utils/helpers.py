import streamlit as st
import pandas as pd
import toml
import os
import snowflake.connector

# Define the order of months for consistent display
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

# GitHub base path once 
GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"


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

    # Get previously selected states and months from session state or fallback to empty list
    default_states = st.session_state.get("selected_states", [])
    default_months = st.session_state.get("selected_months", [])

    with st.sidebar:
        # Title
        st.markdown(
            '<h2 style="text-align: left;">Customize Your Exploration</h2>',
            unsafe_allow_html=True
        )

        # Multi-select widget for states
        selected_states = st.multiselect(
            "🗺️ Select State(s):", 
            sorted(states),
            default=default_states,
            key="state_selector"
        )

        # Multi-select widget for months
        selected_months = st.multiselect(
            "📅 Select Month(s):",
            month_order,
            default=default_months,
            key="month_selector"
        )

    # Save selections back to session state for persistence
    st.session_state["selected_states"] = selected_states
    st.session_state["selected_months"] = selected_months

    # Return the current selections
    return selected_states, selected_months
