import streamlit as st
from utils.helpers import render_sidebar

# --- 1. Page Setup ---
st.set_page_config(page_title="India Cultural Experience Explorer", layout="wide")

# --- 2. Title and Intro ---
st.title("🇮🇳 India’s Cultural, Artistic & Heritage Explorer")

st.markdown("""
Welcome to the **India Cultural Experience Explorer** — your interactive gateway to the **art, heritage, and cultural richness** of India.

🎨 **What can you explore?**
- 📍 Discover famous monuments, art, and cultural events across Indian states.
- 📆 Understand the best times to visit using climate data, tourist season insights, and festivals.
- 🌱 Get personalized recommendations for responsible travel.

Start by selecting the **states** and **months** you’re interested in to tailor the report to your preferences.

---           
""")

# Render the sidebar and use the selections
selected_states, selected_months = render_sidebar()

# Use the selected values
st.write("You selected:", selected_states, selected_months)



