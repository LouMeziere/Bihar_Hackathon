import streamlit as st
import pandas as pd
from utils.helpers import render_sidebar
import plotly.graph_objects as go

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import streamlit.components.v1 as components


# Sidebar selections
selected_states, selected_months = render_sidebar()

# Load UNESCO data
unesco_df = pd.read_csv("datasets/unesco_sites_per_country.csv", encoding='windows-1252')

# Sort descending by site amount
unesco_df_sorted = unesco_df.sort_values("site amount", ascending=False).reset_index(drop=True)

# Get India info
india_row = unesco_df_sorted[unesco_df_sorted["countries"] == "India"].reset_index()
india_site_count = int(india_row.at[0, "site amount"])
india_rank = india_row.at[0, "index"] + 1

# Get countries ranked above India (if any)
countries_above = unesco_df_sorted.iloc[:india_rank][["countries", "site amount"]].sort_values("site amount").reset_index(drop=True)

# --- Streamlit UI ---

st.title("What We See")

st.markdown(f"""
<div style="max-width: 900px; margin: auto; padding: 20px; border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%); box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
  <h2 style="color:#ffffff; font-weight: 900; font-size: 3rem; margin-bottom: 0;">India: A Visual Wonderland</h2>
  <p style="font-size: 1.2rem; color:#93aca4; margin-top: 8px;">
    India is a top destination for travelers drawn by its rich tapestry of sights — from stunning temples and majestic forts to breathtaking natural landscapes.
  </p>
  
  <!-- Big stats -->
  <div style="display: flex; justify-content: center; gap: 60px; margin: 40px 0;">
    <div style="text-align: center;">
      <div style="font-size: 60px; font-weight: 900; color:#34f4a4;">{india_site_count}</div>
      <div style="font-weight: 600; color: #ffffff;">UNESCO Sites</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 60px; font-weight: 900; color:#34f4a4;">#{india_rank}</div>
      <div style="font-weight: 600; color: #ffffff;">Global Rank</div>
    </div>
  </div>
""", unsafe_allow_html=True)


# Prepare the data for plotting
countries = countries_above["countries"].tolist()
site_counts = countries_above["site amount"].tolist()

# Create plotly figure with variable name `fig`
fig = go.Figure()

ranks = list(range(len(countries), 0, -1))  # descending from 6 to 1

fig.add_trace(go.Bar(
    x=countries,
    y=site_counts,
    text=[f"<b>{country}</b><br>{int(sites)}" for country, sites in zip(countries, site_counts)],
    textposition='outside',
    textfont=dict(size=12, color='white'),
    marker=dict(
        color='rgba(28, 76, 84, 0.85)',
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
    ),
    width=0.4,
    hoverinfo='text',
    hovertemplate=[
        f'<span style="color:#34f4a4; font-weight:bold;">Global rank:</span> <span style="color:#ffffff;">#{rank}</span><extra></extra>'
        for rank in ranks
    ],
    texttemplate="%{text}",  # This enables HTML in the text
))





fig.update_layout(
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(range=[40, max(site_counts) + 5], showgrid=False, zeroline=False, showticklabels=False),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300
)

# Streamlit container with background and rounded corners for the plot
st.markdown("""
<div style="border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%); padding: 20px;">
""", unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)





# Load datasets
df_culture = pd.read_csv("datasets/cultural_sites.csv", encoding='windows-1252')
df_festival = pd.read_csv("datasets/festivals_data.csv")
df_art = pd.read_csv("datasets/arts.csv", encoding='windows-1252')
#df_ITA = pd.read_csv("datasets/monthwise_ITAs.csv", encoding='windows-1252')
df_weather = pd.read_csv("datasets/weather_data.csv")

df_culture = df_culture.dropna(subset=['latitude', 'longitude'])
df_festival = df_festival.dropna(subset=['state'])


# Apply the same filters to both datasets
if selected_states:
    df_culture = df_culture[df_culture['state'].isin(selected_states)]


# --- Map Setup ---
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles='CartoDB positron')
marker_cluster = MarkerCluster().add_to(m)

# --- Define marker color based on visitors ---
def get_marker_color(visitors):
    try:
        visitors = int(visitors)
        if visitors >= 500_000:
            return "red"
        elif visitors >= 150_000:
            return "orange"  # custom yellow
        else:
            return 'green'
    except:
        return "blue"

# --- Setup GitHub base path once ---
GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"

# --- Construct image_url column once ---
df_culture["image_url"] = df_culture["image_url"].apply(lambda x: f"{GITHUB_BASE}/{x}")


# --- Add markers with UNESCO tag ---
for _, row in df_culture.iterrows():
    color = get_marker_color(row['2023-24 total visitors'])
    
    img_html = f'<img src="{row["image_url"]}" alt="{row["monument"]}" style="width:100%; max-height:120px; object-fit:cover; margin-bottom:8px;" />'

    # UNESCO badge if applicable
    unesco_label = ""
    if str(row.get("unesco", "")).lower() == "true":
        unesco_label = '<span style="background-color:#d4af37; color:#000; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:12px;"><img src="https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main/images/UNESCO_logo.png" alt="" width="17" height="20"> UNESCO Site</span><br>'

    html = f"""
    <div style="width:220px">
        {img_html}
        <h4>{row['monument']}</h4>
        {unesco_label}
        <b>City:</b> {row['city']}<br>
        <b>State:</b> {row['state']}<br>
        <b>Visitors (2023-24):</b> {row['2023-24 total visitors']:,}<br>
        <b>Domestic Growth:</b> {row['% domestic growth']}%
    </div>
    """
    popup = folium.Popup(html, max_width=250)

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        icon=folium.Icon(color=color, icon="university", prefix="fa")
    ).add_to(marker_cluster)

# --- Display Map ---
container_style = """
    max-width: 900px; 
    margin: 30px auto; 
    padding: 24px 28px; 
    border-radius: 12px; 
    background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 100%);
    background-color: #041c1c;  /* fallback */
    box-shadow: 0 4px 12px rgba(0,0,0,0.3); 
    color: #93aca4; 
    font-size: 1.15rem; 
    line-height: 1.6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
"""

# Use st.markdown for the green container background only for the text
with st.container():
    st.markdown(f'<div style="{container_style}">', unsafe_allow_html=True)
    
    st.markdown("""
        <p>India's cultural richness is globally acknowledged, reflected in its many UNESCO World Heritage sites.  
        Explore the map below to uncover the full spectrum of these treasured landmarks across the country.</p>

        <p>However, not all sites receive equal attention. Highly popular destinations, especially in states like <strong>Uttar Pradesh</strong>, <strong>Delhi</strong>, and <strong>Rajasthan</strong>, attract <strong>huge crowds</strong>, which can:</p>

        <ul style="padding-left: 20px; color: #b1c1b7;">
          <li>Strain local infrastructure</li>
          <li>Damage fragile heritage sites</li>
          <li>Make visits less enjoyable for tourists</li>
        </ul>

        <p>Conversely, <strong>culturally rich but less-visited states</strong> like <strong>Bihar</strong>, <strong>Odisha</strong>, and <strong>Chhattisgarh</strong> offer authentic and meaningful experiences — <em>without the crowds.</em></p>
        <hr style="border: 0; border-top: 1px solid #2f5b63; margin: 24px 0;">
        <p style="font-weight: 600; color: #34f4a4; font-size: 1.2rem;">
        💡 Scroll through the map below to explore cultural sites by region.
        </p>

        <ul style="padding-left: 20px; color: #b1c1b7;">
          <li>Click on any site to learn more.</li>
          <li>UNESCO sites are marked with their official logo.</li>
          <li>Marker colors indicate visitor volume: 🟢 low, 🟠 medium, 🔴 high.</li>
        </ul>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Add some vertical spacing between text and map
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

    # Wrap the map in a smaller container with margin to create green space around
    map_container_style = """
        max-width: 750px;
        margin: 0 auto 40px auto;  /* center horizontally + bottom margin */
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        background-color: #0a2a2a;  /* slightly different dark bg for map container */
    """
    st.markdown(f'<div style="{map_container_style}">', unsafe_allow_html=True)
    st_folium(m, width=750, height=600)
    st.markdown('</div>', unsafe_allow_html=True)






# --- 7. Top 3 Most Visited Monuments (Filtered) ---
top_3_monuments = df_culture.sort_values('2023-24 total visitors', ascending=False).head(3)

st.subheader("🏆 Top 3 Most Visited Monuments (2023-24)")
st.markdown("""
Here are the **most visited cultural sites** based on your current state selection — or for **all of India** if no filter is applied.
These monuments are popular for a reason — they’re iconic, historically significant, and architecturally stunning. But here’s your opportunity to go beyond the obvious. 

👉 **Use the filters on your left to discover high-value sites in lesser-visited states** like **Bihar** or **Odisha** — where your visit can have a *greater local impact* and offer a *deeper cultural experience*.
""")
html_content = ""

for i, (_, row) in enumerate(top_3_monuments.iterrows(), start=1):
    html_content += f"""
    <div style="
        background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%);
        padding: 20px 30px;
        border-radius: 10px;
        color: #93aca4;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
    ">
        <!-- Left side: Number and info -->
        <div style="display: flex; flex: 1; gap: 20px; align-items: flex-start;">
            <!-- Number -->
            <div style="
                font-size: 72px;
                font-weight: 900;
                color: #34f4a4;
                line-height: 1;
                user-select: none;
                flex-shrink: 0;
                width: 80px;
                display: flex;
                align-items: flex-end;  /* align number bottom with title */
                justify-content: center;
            ">
                {i:02d}
            </div>
            <!-- Info (title + details) -->
            <div style="display: flex; flex-direction: column; gap: 6px; flex-grow: 1;">
                <div style="font-size: 20px; color: #ffffff; font-weight: bold; line-height: 1.2;">
                    {row['monument']}
                </div>
                <div style="color: #93aca4; font-size: 14px;">
                    <div>📍 {row['city']}, {row['state']}</div>
                    <div>👥 <strong>{row['2023-24 total visitors']:,} visitors</strong></div>
                    <div>📈 Domestic Growth: {row['% domestic growth']}%</div>
                </div>
            </div>
        </div>
        <!-- Right side: Image -->
        <div style="flex-shrink: 0;">
            <img src="{row['image_url']}" width="150" style="border-radius: 8px;" />
        </div>
    </div>
    """





st.markdown(html_content, unsafe_allow_html=True)