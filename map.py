import streamlit as st
import pydeck as pdk
import json


import chardet

with open("datasets/festivals_data.csv", 'rb') as f:
    result = chardet.detect(f.read(10000))
    print(result)




# Load railway lines GeoJSON
with open("datasets/railway/railways_lines.geojson") as f:
    lines_data = json.load(f)

# Load railway points GeoJSON
with open("datasets/railway/railways_points.geojson") as f:
    points_data = json.load(f)

# Define the railway line layer (red lines)
rail_layer = pdk.Layer(
    "GeoJsonLayer",
    lines_data,
    get_line_color=[255, 0, 0],
    get_line_width=2,
    pickable=True
)

# Define the points layer (blue circles)
points_layer = pdk.Layer(
    "GeoJsonLayer",
    points_data,
    get_fill_color=[0, 0, 255, 160],  # Semi-transparent blue
    get_radius=1000,  # Radius in meters
    point_radius_min_pixels=2,
    point_radius_max_pixels=10,
    pickable=True
)

# Set the initial view state
view_state = pdk.ViewState(
    latitude=22.9734,
    longitude=78.6569,
    zoom=4,
    pitch=0
)

# Render the map with both layers
st.pydeck_chart(pdk.Deck(
    layers=[rail_layer, points_layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}"}
))
