import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Load the data
df = pd.read_csv("datasets/cultural_sites.csv", encoding="windows-1252")
df = df.dropna(subset=['latitude', 'longitude'])

# Title
st.title("🗺️ Cultural Heritage Sites in India")
st.markdown("Scroll and click on each point to explore visitor counts.")

# Initialize Folium Map centered on India
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles='CartoDB positron')

# Add marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add markers
for i, row in df.iterrows():
    html = f"""
    <div style="width:220px">
        <h4>{row['monument']}</h4>
        <img src="{row['image_url']}" width="200"><br><br>
        <b>City:</b> {row['city']}<br>
        <b>State:</b> {row['state']}<br>
        <b>2023-24 Total Visitors:</b> {row['2023-24 total visitors']}<br>
        <b>% Domestic Growth:</b> {row['% domestic growth']}%
    </div>
    """
    popup = folium.Popup(html, max_width=250)
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        icon=folium.Icon(color="green", icon="university", prefix="fa")
    ).add_to(marker_cluster)


# Render in Streamlit
st_data = st_folium(m, width=800, height=600)
