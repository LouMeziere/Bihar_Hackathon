import streamlit as st
import pandas as pd
import numpy as np
import os
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
import altair as alt
import plotly.graph_objects as go


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








# Load datasets
df_culture = pd.read_csv("datasets/cultural_sites.csv", encoding='windows-1252')
df_festival = pd.read_csv("datasets/festivals.csv", encoding='windows-1252')
df_art = pd.read_csv("datasets/arts.csv", encoding='windows-1252')
#df_ITA = pd.read_csv("datasets/monthwise_ITAs.csv", encoding='windows-1252')
df_weather = pd.read_csv("datasets/weather_data.csv")

df_culture = df_culture.dropna(subset=['latitude', 'longitude'])
df_festival = df_festival.dropna(subset=['state'])

# Get unique states and months from both datasets
states = pd.concat([df_culture['state'], df_festival['state'], df_art['state'], df_weather['state']]).dropna().unique()
months = df_weather['month'].dropna().unique()  # or just use your predefined all_months list
print(states)
print(months)
with st.sidebar:
    st.header("Customize Your Exploration")

    selected_states = st.multiselect(
        "🗺️ Select State(s):", 
        sorted(states), 
        default=None, 
        placeholder="All States"
    )

    selected_months = st.multiselect(
        "📅 Select Month(s):",
        months,  # or all_months
        default=None,
        placeholder="All Months",
        key="month_selector"
    )

# Apply the same filters to both datasets
if selected_states:
    df_culture = df_culture[df_culture['state'].isin(selected_states)]
    df_festival = df_festival[df_festival['state'].isin(selected_states)]
    df_art = df_art[df_art['state'].isin(selected_states)]
    df_weather = df_weather[df_weather['state'].isin(selected_states)]

if selected_months:
    df_weather = df_weather[df_weather['month'].isin(selected_months)]





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

# --- Add markers with UNESCO tag ---
for _, row in df_culture.iterrows():
    color = get_marker_color(row['2023-24 total visitors'])

    img_html = f'<img src="{row["image_url"]}" alt="{row["monument"]}" style="width:100%; max-height:120px; object-fit:cover; margin-bottom:8px;" />'

    # UNESCO badge if applicable
    unesco_label = ""
    if str(row.get("unesco", "")).lower() == "true":
        unesco_label = '<span style="background-color:#d4af37; color:#000; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:12px;"><img src="images/UNESCO_logo.png" alt="unesco logo" width="10" height="12"> UNESCO Site</span><br>'

    html = f"""
    <div style="width:220px">
        {img_html}
        <h4>{row['monument']}</h4>
        {unesco_label}
        <b>Location:</b> {row['city']}, {row['state']}<br>
        <b>2023-24 Visitors:</b> {row['2023-24 total visitors']:,}<br>
        <b>% Domestic Growth:</b> {row['% domestic growth']}%
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
        image_path = os.path.normpath(row['image_url'].lstrip('/\\'))

        if os.path.exists(image_path):
            st.image(image_path, width=150, caption=row['monument'])
        else:
            st.markdown("🖼️ *Image not found*")
    with col2:
        st.markdown(f"**{row['monument']}**")
        st.markdown(f"📍 {row['city']}, {row['state']}")
        st.markdown(f"👥 **{row['2023-24 total visitors']:,} visitors**")
        st.markdown(f"📈 Domestic Growth: {row['% domestic growth']}%")
    st.markdown("---")









from PIL import Image
import streamlit as st
from streamlit_carousel import carousel

st.subheader("🎨 Traditional Art Forms")
st.markdown(
    "*While traveling, it is recommended to purchase handicrafts and souvenirs directly from the local community or non-profit cooperatives. "
    "This helps support the destination's economy and encourages artisans to preserve and share their cultural heritage.*"
)

arts_filtered = df_art.sort_values(by="state").copy()
if selected_states:
    arts_filtered = arts_filtered[arts_filtered["state"].isin(selected_states)]

if arts_filtered.empty:
    st.info("No traditional art forms found for the selected state(s).")
else:
    items = []
    for _, row in arts_filtered.iterrows():
        if pd.notnull(row["image_url"]):
            image_path = f"images/arts/{row['image_url']}"
            try:
                with Image.open(image_path) as img:
                    # Resize image to desired height while maintaining aspect ratio
                    desired_height = 400
                    aspect_ratio = img.width / img.height
                    new_width = int(desired_height * aspect_ratio)
                    resized_img = img.resize((new_width, desired_height))
                    # Save or process the resized image as needed
                    # For demonstration, we'll assume the image is saved and accessible via a URL
                    resized_image_url = f"resized_images/{row['image_url']}"
            except Exception as e:
                resized_image_url = "https://via.placeholder.com/400x300?text=No+Image"
        else:
            resized_image_url = "https://via.placeholder.com/400x300?text=No+Image"

        items.append({
            "title": f"{row['name']}",
            "text": f"📍 {row['state']}",
            "img": resized_image_url
        })

    carousel(items)















import calendar

st.subheader("Experiences of a life time")

# Ensure datetime columns
df_festival["start date"] = pd.to_datetime(df_festival["start date"], errors="coerce")
df_festival["end date"] = pd.to_datetime(df_festival["end date"], errors="coerce")

# Apply filters
filtered_festivals = df_festival.copy()

if selected_states:
    filtered_festivals = filtered_festivals[filtered_festivals["state"].isin(selected_states)]

if selected_months:
    month_number_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    selected_month_nums = [month_number_map[m] for m in selected_months]
    filtered_festivals = filtered_festivals[
        filtered_festivals["start date"].dt.month.isin(selected_month_nums)
    ]

# Combine entries with the same festival but different states
grouped = (
    filtered_festivals
    .groupby(["festival", "start date", "end date", "description"], dropna=False)
    .agg({"state": lambda x: ", ".join(sorted(set(x.dropna())))})
    .reset_index()
)

# Sort by start date
grouped = grouped.sort_values(by="start date")








import calendar

# Step 1: Get available (year, month) pairs
available_months = sorted(grouped["start date"].dropna().apply(lambda d: (d.year, d.month)).unique())

# Step 2: Initialize session state
if "month_index" not in st.session_state:
    st.session_state.month_index = 0

# Step 3: Add navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Previous"):
        if st.session_state.month_index > 0:
            st.session_state.month_index -= 1
with col3:
    if st.button("Next →"):
        if st.session_state.month_index < len(available_months) - 1:
            st.session_state.month_index += 1

# Step 4: Display festivals for current month only
if available_months:
    selected_year, selected_month = available_months[st.session_state.month_index]
    st.subheader(f"📅 Festivals in {calendar.month_name[selected_month]} {selected_year}")

    this_month = grouped[
        (grouped["start date"].dt.year == selected_year) &
        (grouped["start date"].dt.month == selected_month)
    ].reset_index(drop=True)

    cards_per_row = 3
    for i in range(0, len(this_month), cards_per_row):
        row_festivals = this_month.iloc[i : i + cards_per_row]
        cols = st.columns(cards_per_row)

        for col, (_, row) in zip(cols, row_festivals.iterrows()):
            with col:
                st.markdown(f"### {row['festival']}")
                start = row['start date'].date()
                end = row['end date'].date() if pd.notnull(row['end date']) else None
                date_str = f"{start}" if not end or start == end else f"{start} → {end}"
                st.markdown(f"**📍 State(s):** {row['state']}")
                st.markdown(f"**📆 Date:** {date_str}")

                with st.expander(f"Details"):
                    st.markdown(row['description'])
                st.markdown("---")
else:
    st.info("No festival data available.")












st.subheader("🌍 Hidden Gems: Why Some Culturally Rich States Are Overlooked")
st.markdown("""
States like **Bihar**, **Odisha**, and **Chhattisgarh** are home to **ancient empires**, **sacred sites**, and **rich artisanal traditions** — yet they receive only a fraction of India’s tourist footfall.

Why?

- Limited tourism infrastructure
- Low media visibility
- Safety or accessibility perceptions
- Over-concentration of promotion in states like Rajasthan or Kerala

🛤️ But things are changing.

Responsible tourism and community-led initiatives are helping these regions gain visibility — not just as “hidden gems,” but as **essential stops for conscious travelers**.

👉 *If you're looking to experience India's cultural soul without the crowds, these states are worth your attention.*
""")









st.subheader("📅 When to Visit: Monthly Travel Trends & Insights")
st.markdown("""
To help travelers make informed and responsible choices, we analyzed **historical weather data (1991–2022)** alongside **monthly visitor trends (2021–2023)**.  
This allows us to identify months that offer **comfortable weather** while avoiding overcrowded periods — promoting a more **sustainable and enjoyable travel experience**.

""")

# Load data
monthwise_ITAs = pd.read_csv("datasets/monthwise_ITAs.csv")

# Clean and reshape
for year in ["2021", "2022", "2023"]:
    monthwise_ITAs[year] = monthwise_ITAs[year].replace(",", "", regex=True).astype(float)

monthwise_ITAs_melted = monthwise_ITAs.melt(
    id_vars=["Months"], value_vars=["2021", "2022", "2023"],
    var_name="Year", value_name="ITAs"
)

# Remove NaNs/zero
monthwise_ITAs_melted = monthwise_ITAs_melted[monthwise_ITAs_melted["ITAs"] > 0]

# Month mapping: full to abbreviated
month_abbrev = {
    "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr",
    "May": "May", "June": "Jun", "July": "Jul", "August": "Aug",
    "September": "Sep", "October": "Oct", "November": "Nov", "December": "Dec"
}

# Filter and apply abbreviation
monthwise_ITAs_melted = monthwise_ITAs_melted[
    monthwise_ITAs_melted["Months"].isin(months)
].copy()
monthwise_ITAs_melted["Months"] = monthwise_ITAs_melted["Months"].map(month_abbrev)

# Set month order with abbreviations
month_order = [month_abbrev[m] for m in months]
monthwise_ITAs_melted["Months"] = pd.Categorical(monthwise_ITAs_melted["Months"], categories=month_order, ordered=True)

# Calculate mean and std per month
avg_visitors = (
    monthwise_ITAs_melted.groupby("Months").agg(
        average=("ITAs", "mean"),
        stddev=("ITAs", "std")
    ).reset_index()
)
avg_visitors["lower"] = avg_visitors["average"] - avg_visitors["stddev"]
avg_visitors["upper"] = avg_visitors["average"] + avg_visitors["stddev"]

# Categorize visitor levels
def categorize_visitors(avg):
    if avg >= avg_visitors["average"].quantile(0.66):
        return "High"
    elif avg >= avg_visitors["average"].quantile(0.33):
        return "Medium"
    else:
        return "Low"

avg_visitors["visitor_category"] = avg_visitors["average"].apply(categorize_visitors)

# Map the selected full month names from the sidebar
selected_months_abbrev = [month_abbrev[m] for m in selected_months if m in month_abbrev]

# X-axis domain helper
def rotate_month_order(center_month, months):
    n = len(months)
    center_idx = months.index(center_month)
    left_count = n // 2 - 1
    rotated = months[center_idx - left_count:] + months[:center_idx - left_count]
    return rotated

# Determine domain
if selected_months_abbrev:
    first_selected = selected_months_abbrev[0]
    x_domain = rotate_month_order(first_selected, month_order)
else:
    x_domain = month_order

# Max y scale and padding
max_upper = avg_visitors["upper"].max()
max_upper_padded = max_upper * 1.125
padding = max_upper * 0.2  # 25% padding on top and bottom

avg_visitors["lower_padded"] = avg_visitors["lower"] - padding
avg_visitors["upper_padded"] = avg_visitors["upper"] + padding

# Prepare highlight outlines (boxes)
highlight_outlines = alt.Chart(avg_visitors[avg_visitors["Months"].isin(selected_months_abbrev)]).mark_rect(
    fill=None,
    stroke="#60a5fa",
    strokeWidth=2
).encode(
    x=alt.X("Months:N", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("lower_padded:Q", scale=alt.Scale(domain=[0, max_upper_padded])),
    y2="upper_padded:Q"
) if selected_months_abbrev else alt.Chart().mark_rect().encode()

# Std Deviation area
std_area = alt.Chart(avg_visitors).mark_area(opacity=0.35, color="#60a5fa").encode(
    x=alt.X("Months:N", scale=alt.Scale(domain=x_domain)),
    y="lower:Q",
    y2="upper:Q"
)

# Base line
base = alt.Chart(avg_visitors).mark_line(
    point=alt.OverlayMarkDef(opacity=0.3),
    color="lightgray"
).encode(
    x=alt.X("Months:N", title="Month", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("average:Q", title="Avg. Tourist Arrivals"),
    tooltip=["Months", "average", "stddev"]
)

# Highlighted line
highlight_df = avg_visitors[avg_visitors["Months"].isin(selected_months_abbrev)].copy()
highlight_line = alt.Chart(highlight_df).mark_line(point=True, color="#F97316").encode(
    x=alt.X("Months:N", scale=alt.Scale(domain=x_domain)),
    y="average:Q",
    detail="Months:N"
)

# Add text labels above boxes
highlight_df["text_y"] = highlight_df["upper_padded"] + padding * 0.1
highlight_text = alt.Chart(highlight_df).mark_text(
    align="center",
    dy=-10,
    fontWeight="bold",
    color="#F97316"
).encode(
    x=alt.X("Months:N", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("text_y:Q"),
    text="visitor_category:N"
)

# Compose final chart
chart = alt.layer(
    highlight_outlines,
    std_area,
    base,
    highlight_line,
    highlight_text
).properties(
    width=700,
    height=400,
    title="📈 Avg. Monthly Tourist Arrivals in India (2021–2023)"
).configure_axisX(labelAngle=0)

# Render in Streamlit
st.altair_chart(chart, use_container_width=True)












# Ensure month column is ordered using full names
df_weather["month"] = pd.Categorical(df_weather["month"], categories=months, ordered=True)

# --- 8. Monthly Weather Insights ---
st.subheader("🌤️ Monthly Weather Insights")

# User filters
selected_months_list = selected_months if selected_months else []

# Recommended base states and months (low tourist + high cultural value)
recommended_states = ["Odisha", "Chhattisgarh", "Nagaland", "Mizoram", "Sikkim"]
recommended_months = ["February", "March", "April", "November"]

# Determine filter mode
base_recommendation_mode = not selected_states and not selected_months_list

# Start filtering
if base_recommendation_mode:
    st.info("✨ Showing recommended destinations for responsible tourism with rich culture and pleasant weather.")
    filtered_df = df_weather[
        (df_weather["state"].isin(recommended_states)) &
        (df_weather["month"].isin(recommended_months))
    ]
else:
    filtered_df = df_weather.copy()
    if selected_states:
        filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]
    if selected_months_list:
        filtered_df = filtered_df[filtered_df["month"].isin(selected_months_list)]

    # Provide feedback on user choices
    def evaluate_user_choices(states, months):
        messages = []
        touristy_states = ["Goa", "Kerala", "Rajasthan", "Uttar Pradesh", "Maharashtra"]

        for month in months:
            subset = df_weather[df_weather["month"] == month]
            if not subset.empty:
                avg_temp = subset["Max Temperature (°C)"].mean()
                avg_rain = subset["Rainfall (mm)"].mean()
                if avg_temp > 35:
                    messages.append(f"🌡️ {month} tends to be very hot. Consider cooler months like February or November.")
                if avg_rain > 150:
                    messages.append(f"🌧️ {month} often has heavy rainfall. Consider dry months like March or December.")

        for state in states:
            if state in touristy_states:
                messages.append(f"🌍 {state} is popular but can get crowded. For a more peaceful experience, try Sikkim or Odisha.")

        if not messages:
            messages.append("👍 Great selection! Your choices offer a nice balance of weather and cultural richness.")
        return messages

    if selected_states or selected_months_list:
        feedback = evaluate_user_choices(selected_states, selected_months_list)
        for msg in feedback:
            st.info(msg)

# If filtered_df is empty, show a message
if filtered_df.empty:
    st.info("No weather data found for the selected filters.")
else:
    # Add weather quality scoring
    def score_destination(row):
        score = 0
        if 20 <= row["Max Temperature (°C)"] <= 30:
            score += 1
        if row["Rainfall (mm)"] < 50:
            score += 1
        if row["Humidity (%)"] < 60:
            score += 1
        return score

    filtered_df["score"] = filtered_df.apply(score_destination, axis=1)

    # Select top 10 cities (or one per state)
    top_df = (
        filtered_df.sort_values(by="score", ascending=False)
        .groupby("state", as_index=False)
        .first()
        .head(10)
    )

    # Rainfall classification
    def rainfall_level(mm):
        if mm < 20:
            return "Low"
        elif mm < 100:
            return "Medium"
        else:
            return "High"

    rainfall_colors = {
        "Low": "#a3d9a5",
        "Medium": "#f5de78",
        "High": "#f28c8c"
    }

    # Card generator
    def generate_card(row):
        rain_level = rainfall_level(row["Rainfall (mm)"])
        rain_color = rainfall_colors[rain_level]
        return f"""
        <div style="
            background-color: #222;
            border-radius: 12px;
            padding: 15px;
            margin: 10px;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            font-family: Arial, sans-serif;
            width: 320px;
            flex-shrink: 0;
        ">
            <h3 style="margin-bottom: 8px;">{row['city']}, {row['state']}</h3>
            <h4 style="margin-top: 0; margin-bottom: 12px;">Month: {row['month']}</h4>
            <p><strong>High:</strong> {row['Max Temperature (°C)']}°C | 
               <strong>Low:</strong> {row['Min Temperature (°C)']}°C</p>
            <p><strong>Rainfall:</strong> <span style="background-color:{rain_color};
                color:#000; padding:2px 6px; border-radius:4px;">{rain_level}</span> 
                ({row['Rainfall (mm)']} mm)</p>
            <p><strong>Humidity:</strong> {row['Humidity (%)']}%</p>
        </div>
        """

    # Render cards in horizontal scroll container
    st.markdown('<div style="display: flex; overflow-x: auto;">', unsafe_allow_html=True)
    for _, row in top_df.iterrows():
        st.markdown(generate_card(row), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
