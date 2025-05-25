# -------------------------------
#           Imports
# -------------------------------

import streamlit as st
from utils.helpers import render_sidebar, GITHUB_BASE


# -------------------------------
#          Page Config
# -------------------------------

st.set_page_config(page_title="India Cultural Explorer", layout="wide")


# -------------------------------
#          Intro Section
# -------------------------------

# Title
st.markdown("""
<div style="text-align: left; margin-top: 40px; margin-bottom: 0px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">India's </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">Cultural Explorer</span>
</div>
""", unsafe_allow_html=True)



# Video of world
st.video(f"{GITHUB_BASE}/images/world.mp4")


# ---------- What You Can Explore ----------
st.markdown("""
<div style="
    background-color:#041c1c;
    border-left: 6px solid #34f4a4;
    padding: 30px 30px 30px 24px;
    border-radius: 10px;
    margin: 40px auto;
    max-width: 900px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
">
    <h2 style="color:#34f4a4; margin-bottom: 20px;">🎨 What can you explore?</h2>
    <ul style="font-size: 18px; line-height: 1.8; color:#ffffff; margin-bottom: 20px; padding-left: 20px;">
        <li><b>📍 Discover:</b> Famous monuments, art, and cultural events across Indian states.</li>
        <li><b>📆 Plan:</b> Understand the best times to visit using climate data, tourist seasons, and festivals.</li>
        <li><b>🌱 Travel Smart:</b> Get personalized recommendations for responsible and ethical travel.</li>
    </ul>
    <p style="font-size: 16px; color:#93aca4;">
        Start by selecting the <b>states</b> and <b>months</b> you’re interested in to tailor the report to your preferences.
    </p>
</div>
""", unsafe_allow_html=True)



# ---------- Visual Steps Cards ----------
col1, col2, col3 = st.columns(3)

card_style = """
padding:20px;
background-color:#1c4c54;
border-radius:10px;
text-align:center;
box-shadow: 0 2px 6px rgba(0,0,0,0.3);
color:#ffffff;
"""

with col1:
    st.markdown(f"""
    <div id="where" style="{card_style}">
        <h3 style="color:#34f4a4;">🌍 Step 1</h3>
        <p><b>Select States & Sites</b><br>Choose Indian states and monuments of interest.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div id="when" style="{card_style}">
        <h3 style="color:#34f4a4;">📅 Step 2</h3>
        <p><b>Pick Travel Months</b><br>See climate, events, and tourist seasons.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div id="how" style="{card_style}">
        <h3 style="color:#34f4a4;">🧭 Step 3</h3>
        <p><b>Get Travel Insights</b><br>Explore festivals, trends & sustainability tips.</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
#          Sidebar Logic
# -------------------------------

selected_states, selected_months = render_sidebar()
