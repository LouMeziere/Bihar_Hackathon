import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils.helpers import render_sidebar


selected_states, selected_months = render_sidebar()


# Load datasets
df_culture = pd.read_csv("datasets/cultural_sites.csv", encoding='windows-1252')
df_festival = pd.read_csv("datasets/festivals_data.csv")
df_art = pd.read_csv("datasets/arts.csv", encoding='windows-1252')
#df_ITA = pd.read_csv("datasets/monthwise_ITAs.csv", encoding='windows-1252')
df_weather = pd.read_csv("datasets/weather_data.csv")

df_culture = df_culture.dropna(subset=['latitude', 'longitude'])
df_festival = df_festival.dropna(subset=['state'])





# --- Load the CSV with UNESCO site counts per country ---
unesco_df = pd.read_csv("datasets/unesco_sites_per_country.csv", encoding='windows-1252')

# Get India's UNESCO site count and global rank
unesco_df_sorted = unesco_df.sort_values("site amount", ascending=False).reset_index(drop=True)
india_row = unesco_df_sorted[unesco_df_sorted["countries"] == "India"].reset_index()
india_site_count = int(india_row.at[0, "site amount"])
india_rank = india_row.at[0, "index"] + 1





# --- 4. Initialize Folium Map ---

st.subheader("🗺️ Explore All Cultural Sites Across India")

st.markdown(f"""
India is home to **{india_site_count} UNESCO World Heritage Sites**, ranking **#{india_rank} globally** for the highest number of listed cultural and natural heritage locations.  
From ancient temples and royal forts to unique architectural marvels, these sites are a testament to India’s rich history and cultural legacy.  
However, not all of them receive equal attention. Highly popular sites, especially in states like Uttar Pradesh, Delhi, or Rajasthan, attract **huge crowds**, which can:
- Strain local infrastructure
- Damage fragile heritage sites
- Make the experience less enjoyable for visitors

On the other hand, **culturally rich but less-visited states** like **Bihar**, **Odisha**, or **Chhattisgarh** offer authentic, meaningful experiences — without the crowds.

---

💡 **Scroll through the map below to explore cultural sites by region.**
- Click on a site to learn more about it.
- Marker colors indicate visitor volume (🟢 low, 🟠 medium, 🔴 high).

""")



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
            return "orange"
        else:
            return "green"
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
with st.container():
    st_data = st_folium(m, width=800, height=600)

# --- Style Fix for iframe height ---
st.markdown("""
    <style>
    iframe {
        height: 600px !important;
        min-height: 600px !important;
        max-height: 600px !important;
    }
    .element-container:has(iframe) {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
        height: 600px !important;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)













# --- 7. Top 3 Most Visited Monuments (Filtered) ---
st.subheader("🏆 Top 3 Most Visited Monuments (2023-24)")
st.markdown("""
Here are the **most visited cultural sites** based on your current state selection — or for **all of India** if no filter is applied.
These monuments are popular for a reason — they’re iconic, historically significant, and architecturally stunning. But here’s your opportunity to go beyond the obvious. 

👉 **Use the filters on your left to discover high-value sites in lesser-visited states** like **Bihar** or **Odisha** — where your visit can have a *greater local impact* and offer a *deeper cultural experience*.
""")

# Sort and select top 3 from filtered data
top_3_monuments = df_culture.sort_values('2023-24 total visitors', ascending=False).head(3)


for _, row in top_3_monuments.iterrows():
    col1, col2 = st.columns([1, 2])
    with col1:
        # Clean relative image path (remove leading slash/backslash if any)
        image_url = row['image_url'] # already the full raw GitHub URL

        if image_url:  # simple check in case it's empty or None
            st.image(image_url, width=150, caption=row['monument'])
        else:
            st.markdown("🖼️ *Image not found*")
    with col2:
        st.markdown(f"**{row['monument']}**")
        st.markdown(f"📍 {row['city']}, {row['state']}")
        st.markdown(f"👥 **{row['2023-24 total visitors']:,} visitors**")
        st.markdown(f"📈 Domestic Growth: {row['% domestic growth']}%")
    st.markdown("---")




