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

from utils.helpers import inject_global_css

inject_global_css()




# -------------------------------
#          Intro Section
# -------------------------------

# Display options of states and months in side bar
selected_states, selected_months = render_sidebar()

# Title
st.markdown("""
<div style="text-align: left; margin: 40px auto; max-width:850px">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHERE </span>
  <span style="color: white; font-size: 54px; font-weight: 600;">the journey begins</span>
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
<div class="container" style="border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #2f5454 50%, #041c1c 100%); box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
  <h2>India: A Visual Wonderland</h2>
  <p style="margin-top: 8px;">
    India is not just a destination — it is an experience. With one of the world’s highest concentrations of UNESCO World Heritage sites, it is a place where culture comes alive.
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
    font=dict(
        family="Arial, sans-serif",   # font family
        size=12,                      # base font size in pixels
    ),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(range=[40, max(site_counts) + 5], showgrid=False, zeroline=False, showticklabels=False),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300
)

# Add small box under
st.markdown("""
<div style="display: flex; justify-content: center;">
  <div style="border-radius: 12px; background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%);
              padding: 20px; max-width: 850px; width: 100%;">
""", unsafe_allow_html=True)


# Close container
st.markdown("""</div></div>""", unsafe_allow_html=True)


# Export the figure as HTML
fig_html = fig.to_html(include_plotlyjs='cdn', full_html=False)

# Wrap in a single div with max-width and center alignment
html = f"""
<div style="max-width: 880px; margin: 0 auto;">
    {fig_html}
</div>
"""

# Render the wrapped chart in Streamlit in one single call
components.html(html, height=350)





# -------------------------------
#     Heritage Sites Section
# -------------------------------

# Sub-title 
st.markdown("""
<h2 style="margin: 40px auto 20px auto;">Exploring India’s Timeless Heritage</h2>
""", unsafe_allow_html=True)


#  --- Load & clean data ---

df_sites = load_table("cultural_sites")

# Drop sites without coordinates
df_sites = df_sites.dropna(subset=['latitude', 'longitude'])



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
<div class=container style="margin-bottom: 24px; background: linear-gradient(to right, #1e2f2f, #1c4c54);
            border-radius: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 40px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            max-width: 850px;">

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
"""

# Render the visitor warning box in Streamlit
st.markdown(visitor_volume_html, unsafe_allow_html=True)

# Add a divider and exploration tips for the map below
st.markdown("""
<div class=container>

  <!-- Divider line -->
  <div style="
      height: 1px; 
      background-color: #2f5b63; 
      border-radius: 1px;
      margin-bottom: 16px;
  "></div>
  
  <!-- Text content -->
  <p style="font-weight: 600; color: #34f4a4; margin-bottom: 8px;">
    💡 Scroll through the map below to explore cultural sites by region.
  </p>
  <p style="margin-bottom: 16px;">
    Keep in mind to avoid highly popular destinations and prioritize <strong>culturally rich but less-visited states</strong> like <strong>Bihar</strong>, <strong>Odisha</strong>, and <strong>Chhattisgarh</strong> for authentic experiences — <em>without the crowds.</em>
  </p>
  
  <ul style="padding-left: 20px; color: #b1c1b7;">
    <li>Click on any site to learn more.</li>
    <li>UNESCO sites are indicated.</li>
    <li>Marker colors indicate visitor volume: 🟢 low, 🟠 medium, 🔴 high.</li>
  </ul>

</div>
""", unsafe_allow_html=True)






# Only keep the instances from state(s) of interest
if selected_states:
    df_sites = df_sites[df_sites['state'].isin(selected_states)]


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
        unesco_label = '<span style="background-color:#93aca4; color:#000; padding:5px 6px; border-radius:4px; font-weight:bold; font-size:12px; display: inline-block; margin-bottom:8px;">🌎 UNESCO Site</span><br>'

    html_monuments = f"""
    <div style="width:220px;">
        {img_html}
        <h4>{row['monument']}</h4>
        {unesco_label}
        <b">City:</b> {row['city']}<br>
        <b>State:</b> {row['state']}<br>
        <b>Visitors (2023-24):</b> {row['total_visitors_2023_24']:,}<br>
        <b>Domestic Growth:</b> {row['domestic_growth_percent']}%
    </div>
    """
    popup = folium.Popup(html_monuments, max_width=250)

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        icon=folium.Icon(color=color, icon="university", prefix="fa")
    ).add_to(marker_cluster)

# Center the map using Streamlit layout
left, center, right = st.columns([1, 6, 1])
with center:
    folium_static(m, width=750, height=650)





# -------------------------------
# Most Visited Monuments Section
# -------------------------------

# Filter monuments based on the selected states (if any)
if selected_states:
    filtered_sites = df_sites[df_sites['state'].isin(selected_states)]
else:
    filtered_sites = df_sites

# Select top 3 monuments based on total visitors in 2023–24 from filtered data
top_3_monuments = filtered_sites.sort_values('total_visitors_2023_24', ascending=False).head(3)

# Render section heading for Top 3 Monuments
st.markdown("""
<h2 style="font-size: 44px; margin: 60px auto 20px auto;">🏆 Top 3 Most Visited Monuments</h2>
""", unsafe_allow_html=True)

# Display introductory text and call to explore lesser-known states
st.markdown("""
<div style="max-width: 850px; margin: 0px auto 60px auto">
  <p>Here are the <strong>most visited cultural sites</strong> based on your current state selection — or for <strong>all of India</strong> if no filter is applied.</p>

  <p>👉 <strong>Use the filters on your left to discover high-value sites in lesser-visited states</strong> like <strong>Bihar</strong> or <strong>Odisha</strong> — where your visit can have a <em>greater local impact</em> and offer a <em>deeper cultural experience</em>.</p>
</div>
""", unsafe_allow_html=True)

# Initialize HTML content string for the top 3 cards
html_content = ""

# Loop through the top 3 monuments and build styled HTML blocks for each
for i, (_, row) in enumerate(top_3_monuments.iterrows(), start=1):
    html_content += f"""
    <div class="container" style="
        background: linear-gradient(to right, #041c1c, #1c4c54);
        padding: 20px 30px;
        border-radius: 10px;
        color: #93aca4;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        max-width: 700px;
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
                align-items: flex-end;
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

# Check if there are monuments to show, display message or the monuments
if top_3_monuments.empty:
    st.info("No monuments found for this selection.")
else:
    st.markdown(html_content, unsafe_allow_html=True)





st.markdown('</div>', unsafe_allow_html=True)