import streamlit as st
import pandas as pd
import toml
import snowflake.connector


month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

# GitHub base path once
GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"



def connect_to_snowflake():
    secrets = toml.load('/Users/loumeziere/Desktop/secret_files/secrets.toml')
    conn_info = secrets['connections']['my_example_connection']
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
    conn = connect_to_snowflake()
    query = f'SELECT * FROM {schema}.{table_name}'
    df = pd.read_sql(query, conn)
    conn.close()
    df.columns = [col.lower() for col in df.columns]
    return df


@st.cache_data
def load_all_data():
    df_site = load_table("cultural_sites")
    df_festival = load_table("festivals_data")
    df_art = load_table("arts")
    df_weather = load_table("weather_data")
    return df_site, df_festival, df_art, df_weather



def render_sidebar():
    df_culture, df_festival, df_art, df_weather = load_all_data()

    # Collect unique state and month values
    states = pd.concat([
        df_culture['state'], 
        df_festival['state'], 
        df_art['state'], 
        df_weather['state']
    ]).dropna().unique()

    

    # Fallback to empty list if not set
    default_states = st.session_state.get("selected_states", [])
    default_months = st.session_state.get("selected_months", [])

    with st.sidebar:
        st.header("🎛️ Customize Your Exploration")

        selected_states = st.multiselect(
            "🗺️ Select State(s):", 
            sorted(states),
            default=default_states,
            key="state_selector"
        )

        selected_months = st.multiselect(
            "📅 Select Month(s):",
            month_order,
            default=default_months,
            key="month_selector"
        )

    # Update session state
    st.session_state["selected_states"] = selected_states
    st.session_state["selected_months"] = selected_months

    return selected_states, selected_months
