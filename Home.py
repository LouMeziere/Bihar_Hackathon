# -------------------------------
#           Imports
# -------------------------------

import streamlit as st
import streamlit.components.v1 as components
from utils.helpers import render_sidebar, GITHUB_BASE




# -------------------------------
#          Intro Section
# -------------------------------

# Page configuration
st.set_page_config(page_title="India Cultural Explorer", layout="wide")

# Title
st.markdown("""
<div style="text-align: left; margin-top: 40px; margin-bottom: 0px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">India's </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">Cultural Explorer</span>
</div>
""", unsafe_allow_html=True)





# -------------------------------
#          Video Section
# -------------------------------

# Display video with file names
st.markdown(f"""
<style>
.container {{
    position: relative;
    width: 700px;
    height: 450px;
    margin: auto;
    overflow: hidden;
    border-radius: 20px;
}}

.container video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: left 50%;  /* vertical center tweak */
    border-radius: 20px;
}}

.text-overlay {{
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    color: white;
    text-align: right;
    font-family: Arial, sans-serif;
    font-weight: bold;
    pointer-events: none;
    max-width: 350px;
}}

.text-overlay div {{
    margin-bottom: 10px;
    font-size: 20px;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
}}
            
/* Style the highlighted words */
.highlight {{
    color: #34f4a4;
}}
</style>

<div class="container">
  <video autoplay loop muted playsinline>
    <source src="{GITHUB_BASE}/static/world.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <div class="text-overlay">
    <div><span class="highlight">Where</span> the journey begins</div>
    <div><span class="highlight">When</span> the journey begins</div>
    <div><span class="highlight">How</span> the journey goes</div>
  </div>
</div>
""", unsafe_allow_html=True)











# -------------------------------
#         Explore Section
# -------------------------------

# Highlighted list of three key travel features
html_code = """
<div style="max-width: 900px; margin: 60px 0 80px 0; font-family: system-ui, sans-serif;">
  <h2 style="color:#ffffff; font-weight: 900; font-size: 44px; margin-bottom: 20px;">
    What can you explore?
  </h2>
  <p style="font-size: 16px; color:#93aca4; margin: 30px 0; line-height: 1.6;">
    <b>India's Cultural Explorer</b> is a visual guide and interactive tool for travelers interested in exploring the cultural, historical, and environmental richness of India. The platform helps users answer essential questions about their journey — <b>where to go</b>, <b>when to go</b>, and <b>how to travel responsibly</b>.
  </p>
  <div style="
    background-color:#041c1c;
    border-left: 6px solid #34f4a4;
    padding: 30px 30px 30px 24px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    font-size: 18px; 
    line-height: 1.7; 
    color:#ffffff; 
    margin-bottom: 24px;
    color: #93aca4;
  ">
    <div style="margin-bottom: 10px;">
      <span style="margin-right: 10px;">📍</span>
      <b style='color: #ffffff;'>Discover:</b> Art, landmarks, and cultural experiences in every state.
    </div>
    <div style="margin-bottom: 10px;">
      <span style="margin-right: 10px;">📆</span>
      <b style='color: #ffffff;'>Plan:</b> Find the best times using weather and festivals.
    </div>
    <div>
      <span style="margin-right: 10px;">🌱</span>
      <b style='color: #ffffff;'>Travel Smart:</b> Get tips for conscious and ethical journeys.
    </div>
  </div>
</div>
"""

# Display
components.html(html_code, height=500, scrolling=False)






# -------------------------------
#      App Files Section
# -------------------------------

# Display 3 cards in 1 row
col1, col2, col3 = st.columns(3)

card_style = """
padding:20px;
background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 80%, #041c1c 100%);
border-radius:10px;
text-align:center;
box-shadow: 0 2px 6px rgba(0,0,0,0.3);
color:#ffffff;
"""

# Column 1: WHERE — Helps users select destinations
with col1:
    st.markdown(f"""
    <div id="where" style="{card_style}">  <!-- Card container with shared style -->
        <h3 style="color:#34f4a4;">01  WHERE</h3>  <!-- Step title in highlight color -->
        <p>Choose the Indian states that call to your heart — from coastal paradises to mountain escapes.</p>
        <!-- Description encourages emotional and geographic variety -->
    </div>
    """, unsafe_allow_html=True)

# Column 2: WHEN — Helps users choose the ideal time
with col2:
    st.markdown(f"""
    <div id="when" style="{card_style}">
        <h3 style="color:#34f4a4;">02  WHEN</h3>
        <p>Pick the best months to explore — based on climate, festivals, and your vibe.</p>
        <!-- Describes time selection with a friendly, modern tone -->
    </div>
    """, unsafe_allow_html=True)

# Column 3: HOW — Encourages mindful travel
with col3:
    st.markdown(f"""
    <div id="how" style="{card_style}">
        <h3 style="color:#34f4a4;">03  HOW</h3>
        <p>Discover soulful ways to travel — through local connections and mindful choices.</p>
        <!-- Promotes ethical and emotionally enriching travel -->
    </div>
    """, unsafe_allow_html=True)



# Display options of states and months in side bar
selected_states, selected_months = render_sidebar()
