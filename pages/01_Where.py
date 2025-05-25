# -------------------------------
#          Imports
# -------------------------------

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from streamlit_folium import folium_static
from utils.helpers import render_sidebar, load_table, month_order, GITHUB_BASE

st.markdown(
    """
    <style>
    .stApp {
        background-color: #101414;
        color: #93aca4;
        ...
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
#          Intro Section
# -------------------------------

# Display options of states and months in side bar
selected_states, selected_months = render_sidebar()

# Title
st.markdown("""
<div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHERE </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">the journey begins</span>
</div>
""", unsafe_allow_html=True)




# -------------------------------
#       Why India section
# -------------------------------


# --- Load & clean data ---

df_unesco = load_table("unesco_sites_per_country")


# --- India's importance card ---

# Sort descending by site amount
df_unesco_sorted = df_unesco.sort_values("site_amount", ascending=False).reset_index(drop=True)

# Get India info
india_row = df_unesco_sorted[df_unesco_sorted["countries"] == "India"].reset_index()
india_site_count = int(india_row.at[0, "site_amount"])
india_rank = india_row.at[0, "index"] + 1

st.markdown(f"""
<div style="max-width: 900px; margin: auto; padding: 20px; border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #2f5454 50%, #041c1c 100%); box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
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



# --- Minimalist bar chart ---

# Get countries ranked up to India
top_countries_unesco = df_unesco_sorted.iloc[:india_rank][["countries", "site_amount"]].sort_values("site_amount").reset_index(drop=True)

# Prepare the data for plotting
countries = top_countries_unesco["countries"].tolist()
site_counts = top_countries_unesco["site_amount"].tolist()

# Create plotly figure with variable name `fig`
fig = go.Figure()

ranks = list(range(len(countries), 0, -1))  # descending from 6 to 1

# Add a bar chart trace for UNESCO site counts
fig.add_trace(go.Bar(
    x=countries,
    y=site_counts,
    text=[
        # Format each label with country and styled site count
        f"<br>{country}<br><span style='font-size:15px;font-weight:600;color:#34f4a4;'>{int(sites)}</span><br>"
        for country, sites in zip(countries, site_counts)
    ],
    textposition='outside',
    textfont=dict(size=12, color='white'),  # Label font style
    marker=dict(
        color='rgba(28, 76, 84, 0.85)',  # Bar fill color
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1)  # Subtle border
    ),
    width=0.4,
    hoverinfo='text',
    hovertemplate=[
        # Custom hover with UNESCO rank and no extra box
        f'<span style="color:#34f4a4; font-weight:bold;">UNESCO rank:</span> <span style="color:#ffffff;">#{rank}</span><extra></extra>'
        for rank in ranks
    ],
    texttemplate="%{text}",  # Plain rendering of HTML-style labels
))

# Tweak layout to be clean and dark-transparent
fig.update_layout(
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(range=[40, max(site_counts) + 5], showgrid=False, zeroline=False, showticklabels=False),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300
)

# Wrap the plot in a styled Streamlit container
st.markdown("""
<div style="border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%); padding: 20px;">
""", unsafe_allow_html=True)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Close the container div
st.markdown("</div>", unsafe_allow_html=True)










# -------------------------------
#     Heritage Sites Section
# -------------------------------

# Sub-title 
st.markdown("""
<h2 style="color:#ffffff; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Exploring India’s Timeless Heritage</h2>
""", unsafe_allow_html=True)


#  --- Load & clean data ---

df_sites = load_table("cultural_sites")

# Drop sites without coordinates
df_sites = df_sites.dropna(subset=['latitude', 'longitude'])

# Only keep the instances from state(s) of interest
if selected_states:
    df_sites = df_sites[df_sites['state'].isin(selected_states)]



# --- Avoid crowds card ---

# Group by state and sum visitors for 2023-24
state_visitors = df_sites.groupby('state')['total_visitors_2023_24'].sum().reset_index()

# Sort and get top 3 states
top_3_states = state_visitors.sort_values('total_visitors_2023_24', ascending=False).head(3)

# Calculate total visitors for all states
total_visitors = state_visitors['total_visitors_2023_24'].sum()

# Calculate combined percentage for top 3 states
combined_visitors = top_3_states['total_visitors_2023_24'].sum()
combined_percentage = round((combined_visitors / total_visitors) * 100, 1)

# Get list of top 3 state names, comma separated
top_3_state_names = ", ".join(top_3_states['state'].tolist())

# Custom HTML block highlighting high-visitor states and impact
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

  <!-- Left section: Explanation of overcrowding issues -->
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

  <!-- Right section: Highlight states and percentage -->
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
<!-- Spacer to prevent layout shift -->
<div style="height: 0px; overflow: hidden;"></div>
"""

# Render the visitor warning box in Streamlit
st.markdown(visitor_volume_html, unsafe_allow_html=True)

# Add a divider and exploration tips for the map below
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



# --- Map ---
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles='CartoDB positron')
marker_cluster = MarkerCluster().add_to(m)

# Define marker color based on amount of visitors
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


# Construct column with full path from image_url 
df_sites["image_url"] = df_sites["image_url"].apply(lambda x: f"{GITHUB_BASE}/{x}")


# Add markers with UNESCO tag 
for _, row in df_sites.iterrows():
    color = get_marker_color(row['total_visitors_2023_24'])
    
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
        <b>Visitors (2023-24):</b> {row['total_visitors_2023_24']:,}<br>
        <b>Domestic Growth:</b> {row['domestic_growth_percent']}%
    </div>
    """
    popup = folium.Popup(html, max_width=250)

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        icon=folium.Icon(color=color, icon="university", prefix="fa")
    ).add_to(marker_cluster)

# Start a styled container for the map with dark background, rounded corners, and shadow
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

# Display the Folium map within the styled container
folium_static(m, width=750, height=600)

# Add a hidden spacer to prevent layout jump after the map
st.markdown(
    """<div style="height: 0px; overflow: hidden;"></div>
    """,
    unsafe_allow_html=True
)







# -------------------------------
# Most Visited Monuments Section
# -------------------------------

# Select top 3 monuments based on total visitors in 2023–24
top_3_monuments = df_sites.sort_values('total_visitors_2023_24', ascending=False).head(3)

# Render section heading for Top 3 Monuments
st.markdown("""
<h2 style="color:#ffffff; font-weight: 900; font-size: 44px; margin: 40px 0 10px 0;">🏆 Top 3 Most Visited Monuments</h2>
""", unsafe_allow_html=True)

# Display introductory text and call to explore lesser-known states
st.markdown("""
<div style="padding-bottom: 30px; font-size: 16px;">
  <p>Here are the <strong>most visited cultural sites</strong> based on your current state selection — or for <strong>all of India</strong> if no filter is applied.</p>

  <p>👉 <strong>Use the filters on your left to discover high-value sites in lesser-visited states</strong> like <strong>Bihar</strong> or <strong>Odisha</strong> — where your visit can have a <em>greater local impact</em> and offer a <em>deeper cultural experience</em>.</p>
</div>
""", unsafe_allow_html=True)

# Initialize HTML content string for the top 3 cards
html_content = ""

# Loop through the top 3 monuments and build styled HTML blocks for each
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
                    <div>👥 <strong>{row['total_visitors_2023_24']:,} visitors</strong></div>
                    <div>📈 Domestic Growth: {row['domestic_growth_percent']}%</div>
                </div>
            </div>
        </div>
        <!-- Right side: Image -->
        <div style="flex-shrink: 0; align-self: flex-start; margin-left: auto;">
            <img src="{row['image_url']}" width="150" style="border-radius: 8px;" />
        </div>
    </div>
    """

# Render the combined HTML for all top 3 monuments
st.markdown(html_content, unsafe_allow_html=True)
