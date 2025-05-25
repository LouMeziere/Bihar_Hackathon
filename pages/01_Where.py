import streamlit as st
import pandas as pd
from utils.helpers import render_sidebar
import plotly.graph_objects as go

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from streamlit_folium import folium_static


# Sidebar selections
selected_states, selected_months = render_sidebar()
# --- Setup GitHub base path once ---
GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"


st.markdown("""
<div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHERE </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">the journey begins</span>
</div>
""", unsafe_allow_html=True)



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


st.markdown(f"""
<div style="max-width: 900px; margin: auto; padding: 20px; border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%); box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
  <h2 style="color:#ffffff; font-weight: 900; font-size: 44px; margin-bottom: 0;">India: A Visual Wonderland</h2>
  <p style="font-size: 1.2rem; color:#93aca4; margin-top: 8px;">
    India is not just a destination — it is an experience. With one of the world’s highest concentrations of UNESCO World Heritage sites, it’s a place where culture comes alive.
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
    text=[
    f"<br>{country}<br><span style='font-size:15px;font-weight:600;color:#34f4a4;'>{int(sites)}</span><br>"
    for country, sites in zip(countries, site_counts)
    ],
    textposition='outside',
    textfont=dict(size=12, color='white'),  # Base color & size
    marker=dict(
        color='rgba(28, 76, 84, 0.85)',
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
    ),
    width=0.4,
    hoverinfo='text',
    hovertemplate=[
        f'<span style="color:#34f4a4; font-weight:bold;">UNESCO rank:</span> <span style="color:#ffffff;">#{rank}</span><extra></extra>'
        for rank in ranks
    ],
    texttemplate="%{text}",  # HTML-friendly for hover only — labels render plain
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









# --- Journey through India ---
st.markdown("""
<h2 style="color:#fffff; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Exploring India’s Timeless Heritage</h2>
""", unsafe_allow_html=True)


# --- HIGH VISITOR VOLUMES ---
# Group by state and sum visitors for 2023-24
state_visitors = df_culture.groupby('state')['2023-24 total visitors'].sum().reset_index()

# Sort and get top 3 states
top_3_states = state_visitors.sort_values('2023-24 total visitors', ascending=False).head(3)

# Calculate total visitors for all states
total_visitors = state_visitors['2023-24 total visitors'].sum()

# Calculate combined percentage for top 3 states
combined_visitors = top_3_states['2023-24 total visitors'].sum()
combined_percentage = round((combined_visitors / total_visitors) * 100, 1)

# Get list of top 3 state names, comma separated
top_3_state_names = ", ".join(top_3_states['state'].tolist())

visitor_volume_html = f"""
<div style="background: linear-gradient(to right, #1e2f2f, #1c4c54);
            padding: 24px;
            border-radius: 16px;
            color: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 40px;
            margin: 0 auto 20px auto;
            max-width: 900px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);">

  <!-- Left side: Description -->
  <div style="flex: 1; min-width: 300px;">
    <div style="font-size: 24px; font-weight: 800; margin-bottom: 16px;">
      Avoid High Visitor Volumes
    </div>
    <div style="font-size: 16px; color: #d0d0d0; margin-bottom: 12px;">
      Highly popular destinations attract significant visitor numbers, which can:
    </div>
    <ul style="list-style: none; padding-left: 0; font-size: 16px; line-height: 1.6; color: #b1c1b7;">
      <li>🚧 Strains local infrastructure</li>
      <li>🏛️ Damages heritage sites</li>
      <li>😓 Makes visits less enjoyable</li>
    </ul>
  </div>

  <!-- Right side: Stats -->
  <div style="flex: 0.6; text-align: center;">
    <div style="font-size: 18px; font-weight: 600; color: #9ee0cc; margin-bottom: 8px;">
      Uttar Pradesh, Maharashtra, Delhi
    </div>
    <div style="font-size: 60px; font-weight: 900; color: #34f4a4; margin-bottom: 6px;">
      {combined_percentage:.1f}%
    </div>
    <div style="font-size: 18px; font-weight: 500; color: #ffffff;">
      of total visitors (2023–24)
    </div>
  </div>

</div>
<!-- Force layout compression -->
<div style="height: 0px; overflow: hidden;"></div>
"""

st.markdown(visitor_volume_html, unsafe_allow_html=True)




st.markdown("""
    <hr style="border: 0; border-top: 1px solid #2f5b63; margin: 24px 0;">
    
    <p style="font-weight: 600; color: #34f4a4; font-size: 1.2rem;">
    💡 Scroll through the map below to explore cultural sites by region.
    </p>
    <p>Keep in mind to avoid highly popular destinations and priorities <strong>culturally rich but less-visited states</strong> like <strong>Bihar</strong>, <strong>Odisha</strong>, and <strong>Chhattisgarh</strong> offer authentic and meaningful experiences — <em>without the crowds.</em></p>
    
    <ul style="padding-left: 20px; color: #b1c1b7;">
    <li>Click on any site to learn more.</li>
    <li>UNESCO sites are indicated.</li>
    <li>Marker colors indicate visitor volume: 🟢 low, 🟠 medium, 🔴 high.</li>
    </ul>
""", unsafe_allow_html=True)




# Add some vertical spacing between text and map
st.markdown('<div style="margin-top:0px;"></div>', unsafe_allow_html=True)













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




# Wrap the map in a smaller container with margin to create green space around
# Container around the map
with st.container():
    st.markdown(
        """
        <div style="max-width: 750px;
                    margin: 0 auto 0 auto;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
                    background-color: #0a2a2a;
                    padding: 0;">
        """,
        unsafe_allow_html=True
    )

    # Render the map using folium_static
    folium_static(m, width=750, height=600)

    st.markdown(
        """<div style="height: 0px; overflow: hidden;"></div>

        """,
        unsafe_allow_html=True
    )








# --- 7. Top 3 Most Visited Monuments (Filtered) ---
top_3_monuments = df_culture.sort_values('2023-24 total visitors', ascending=False).head(3)

st.markdown("""
<h2 style="color:#fffff; font-weight: 900; font-size: 44px; margin: 40px 0 10px 0;">🏆 Top 3 Most Visited Monuments</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding-bottom: 30px; font-size: 16px; color: #ffffff;">
  <p>Here are the <strong>most visited cultural sites</strong> based on your current state selection — or for <strong>all of India</strong> if no filter is applied.</p>

  <p>👉 <strong>Use the filters on your left to discover high-value sites in lesser-visited states</strong> like <strong>Bihar</strong> or <strong>Odisha</strong> — where your visit can have a <em>greater local impact</em> and offer a <em>deeper cultural experience</em>.</p>
</div>
""", unsafe_allow_html=True)


html_content = ""

for i, (_, row) in enumerate(top_3_monuments.iterrows(), start=1):
    html_content += f"""
    <div style="
        background: linear-gradient(to right, #041c1c, #1c4c54);
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
        <div style="flex-shrink: 0; align-self: flex-start; margin-left: auto;">
            <img src="{row['image_url']}" width="150" style="border-radius: 8px;" />
        </div>
    </div>
    """





st.markdown(html_content, unsafe_allow_html=True)