import streamlit as st
import pandas as pd
import toml
import snowflake.connector

@st.cache_data
def load_art_data():
    return pd.read_csv("data/arts.csv")

@st.cache_data
def load_all_data():


    df_culture = pd.read_csv("datasets/cultural_sites.csv", encoding='windows-1252')
    df_festival = pd.read_csv("datasets/festivals_data.csv")
    df_art = pd.read_csv("datasets/arts.csv")
    df_weather = pd.read_csv("datasets/weather_data.csv")
    return df_culture, df_festival, df_art, df_weather

def connect_to_snowflake():
    secrets = toml.load('/Users/loumeziere/Desktop/secret_files/secrets.toml')
    conn_info = secrets['connections']['my_example_connection']
    return snowflake.connector.connect(**conn_info)

def render_sidebar():
    df_culture, df_festival, df_art, df_weather = load_all_data()

    # Collect unique state and month values
    states = pd.concat([
        df_culture['state'], 
        df_festival['state'], 
        df_art['state'], 
        df_weather['state']
    ]).dropna().unique()

    months = df_weather['month'].dropna().unique()

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
            sorted(months),
            default=default_months,
            key="month_selector"
        )

    # Update session state
    st.session_state["selected_states"] = selected_states
    st.session_state["selected_months"] = selected_months

    return selected_states, selected_months
