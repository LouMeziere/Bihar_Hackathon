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
- 📍 Discover famous monuments, art centers, and cultural events across Indian states.
- 📆 Understand the best times to visit using climate data, tourist season insights, and festivals.
- 🌱 Get personalized recommendations for responsible travel.

Start by selecting the **states** and **months** you’re interested in to tailor the report to your preferences.
""")

# --- 3. Load and Clean Data ---
df = pd.read_csv("datasets/cultural_sites.csv", encoding="windows-1252")
df = df.dropna(subset=['latitude', 'longitude'])

# --- 4. Sidebar: Filters ---
with st.sidebar:
    st.header("🎛️ Customize Your Exploration")

    # State Filter
    states = df['state'].dropna().unique()
    selected_states = st.multiselect("🗺️ Select State(s):", sorted(states), default=None, placeholder="All States")

    # Month Filter (purely for user preference – not applied to the dataset yet)
    all_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    selected_months = st.multiselect(
        "📅 Select Month(s):",
        all_months,
        default=None,
        placeholder="All Months",
        key="month_selector"
    )


# --- 5. Apply Filters ---
if selected_states:
    filtered_df = df[df['state'].isin(selected_states)]
else:
    filtered_df = df.copy()  # No selection = show all

selected_months = selected_months if selected_months else all_months

# Note: If no month filter is applied or column doesn't exist, keep data as is

# --- 6. Show Filter Summary ---
st.markdown(f"""
### 🎯 Your Current View
- **Selected State(s):** {', '.join(selected_states) if selected_states else 'All'}
- **Selected Month(s):** {', '.join(selected_months) if selected_months else 'All'}
""")

# --- 7. Prompt for Next Sections ---
st.markdown("👇 Scroll down to explore detailed **maps, climate graphs**, and **seasonal recommendations** based on your choices.")



# --- 4. Initialize Folium Map ---
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles='CartoDB positron')
marker_cluster = MarkerCluster().add_to(m)

# --- 5. Add Markers for Selected Monuments ---
for _, row in filtered_df.iterrows():
    # Assuming 'image_url' contains the relative or absolute path to the image
    # Add some inline styling to limit image width or height so popup looks good
    img_html = f'<img src="{row["image_url"]}" alt="{row["monument"]}" style="width:100%; max-height:120px; object-fit:cover; margin-bottom:8px;" />'

    html = f"""
    <div style="width:220px">
        {img_html}
        <h4>{row['monument']}</h4>
        <b>City:</b> {row['city']}<br>
        <b>State:</b> {row['state']}<br>
        <b>2023-24 Total Visitors:</b> {row['2023-24 total visitors']}<br>
        <b>% Domestic Growth:</b> {row['% domestic growth']}%
    </div>
    """
    popup = folium.Popup(html, max_width=250)
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        icon=folium.Icon(color="green", icon="university", prefix="fa")
    ).add_to(marker_cluster)

# --- 6. Display Map in Streamlit ---
with st.container():
    st_data = st_folium(m, width=800, height=600)

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

# Sort and select top 3 from filtered data
top_3_monuments = filtered_df.sort_values('2023-24 total visitors', ascending=False).head(3)


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








import pandas as pd
import altair as alt
import streamlit as st

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
month_order_full = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
month_abbrev = {
    "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr",
    "May": "May", "June": "Jun", "July": "Jul", "August": "Aug",
    "September": "Sep", "October": "Oct", "November": "Nov", "December": "Dec"
}

# Filter and apply abbreviation
monthwise_ITAs_melted = monthwise_ITAs_melted[
    monthwise_ITAs_melted["Months"].isin(month_order_full)
].copy()
monthwise_ITAs_melted["Months"] = monthwise_ITAs_melted["Months"].map(month_abbrev)

# Set month order with abbreviations
month_order = [month_abbrev[m] for m in month_order_full]
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

# UI: select months to highlight
selected_months = st.multiselect("Highlight Months", month_order)

# X-axis domain helper
def rotate_month_order(center_month, months):
    n = len(months)
    center_idx = months.index(center_month)
    left_count = n // 2 - 1
    rotated = months[center_idx - left_count:] + months[:center_idx - left_count]
    return rotated

# Determine domain
if selected_months:
    first_selected = selected_months[0]
    x_domain = rotate_month_order(first_selected, month_order)
else:
    x_domain = month_order

# Max y scale and padding
max_upper = avg_visitors["upper"].max()
max_upper_padded = max_upper * 1.125
padding = max_upper * 0.25  # 25% padding on top and bottom

avg_visitors["lower_padded"] = avg_visitors["lower"] - padding
avg_visitors["upper_padded"] = avg_visitors["upper"] + padding

# Prepare highlight outlines (boxes)
highlight_outlines = alt.Chart(avg_visitors[avg_visitors["Months"].isin(selected_months)]).mark_rect(
    fill=None,
    stroke="#60a5fa",
    strokeWidth=2
).encode(
    x=alt.X("Months:N", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("lower_padded:Q", scale=alt.Scale(domain=[0, max_upper_padded])),
    y2="upper_padded:Q"
) if selected_months else alt.Chart().mark_rect().encode()

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
highlight_df = avg_visitors[avg_visitors["Months"].isin(selected_months)].copy()
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
    title="📈 Avg. Monthly Tourist Arrivals in India (2021–2023) with Std Deviation"
).configure_axisX(labelAngle=0)

# Render in Streamlit
st.altair_chart(chart, use_container_width=True)







##### CARd and temperatures

import streamlit as st
import streamlit as st
import pandas as pd

# Mapping state to capitals
state_to_capital = {
    "Andhra Pradesh": "Amaravati",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Dispur",
    "Bihar": "Patna",
    "Chhattisgarh": "Raipur",
    "Goa": "Panaji",
    "Gujarat": "Gandhinagar",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Odisha": "Bhubaneswar",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata"
}

# Load your dataset (adjust path accordingly)
weather_df = pd.read_csv("datasets/weather_data.csv")

# Normalize month names to short form to match your mapping (Jan, Feb, etc.)
month_full_to_short = {
    "January": "Jan",
    "February": "Feb",
    "March": "Mar",
    "April": "Apr",
    "May": "May",
    "June": "Jun",
    "July": "Jul",
    "August": "Aug",
    "September": "Sep",
    "October": "Oct",
    "November": "Nov",
    "December": "Dec"
}

# Add capital city column
weather_df["capital"] = weather_df["state"].map(state_to_capital)

# Convert month column to categorical with ordering (assuming your dataset uses short month names)
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
weather_df["month"] = pd.Categorical(weather_df["month"], categories=month_order, ordered=True)



# Map selected full month names to short month names used in dataset for filtering
selected_months_short = [month_full_to_short[m] for m in selected_months]

# Filter dataset by selected states and months
filtered_df = weather_df.copy()

if selected_states:
    filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]

if selected_months_short:
    filtered_df = filtered_df[filtered_df["month"].isin(selected_months_short)]

# Helper function for rainfall level and color
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

# Card HTML generator
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
        <h3 style="margin-bottom: 8px;">{row['capital']}, {row['state']}</h3>
        <h4 style="margin-top: 0; margin-bottom: 12px;">Month: {row['month']}</h4>
        <p><strong>High:</strong> {row['Max Temperature (°C)']}°C | <strong>Low:</strong> {row['Min Temperature (°C)']}°C</p>
        <p style="
            background-color: {rain_color};
            color: #222;
            padding: 6px 10px;
            border-radius: 6px;
            font-weight: bold;
            display: inline-block;
        ">
            Rainfall: {row['Rainfall (mm)']} mm ({rain_level})
        </p>
    </div>
    """

# Layout cards in rows of 3
cards_per_row = 3
cards = [generate_card(row) for _, row in filtered_df.iterrows()]

# Show results or message if none
if len(cards) == 0:
    st.warning("No data matches your filter selections.")
else:
    st.markdown("### 🌦️ Weather Data Cards")
    # Create rows of cards
    for i in range(0, len(cards), cards_per_row):
        row_cards = cards[i:i+cards_per_row]
        row_html = "<div style='display: flex; flex-wrap: nowrap; justify-content: flex-start;'>" + "".join(row_cards) + "</div>"
        st.markdown(row_html, unsafe_allow_html=True)











def get_conclusions(selected_months, weather_df, avg_visitors, month_order):
    # Base case: no months selected → fixed text you provided
    if not selected_months:
        return (
            "The main rainfall season occurs from June to September, making these months generally less ideal "
            "for visits due to heavy rain and high humidity. This period also coincides with the hottest weather of "
            "the year, with temperatures often reaching up to 40°C. The best time to visit is from October to April, "
            "when the climate is more pleasant and conducive to outdoor activities. However, January and December see "
            "a significant influx of tourists, leading to crowded sites. To fully enjoy your visit and support "
            "responsible tourism, it's advisable to avoid these peak months and help spread tourism more evenly "
            "throughout the year."
        )

    # Months selected case — ignore Jan and Dec in logic but show if selected
    months_to_consider = [m for m in selected_months if m not in ("January", "December")]

    # If only Jan and/or Dec selected
    if not months_to_consider:
        return "Selected months include January and/or December, which are peak visitor periods with crowded sites. To fully enjoy your visit and promote responsible tourism, it is recommended to avoid these months and help distribute tourism more evenly throughout the year."

    # Filter weather and visitors for selected months
    filtered_weather = weather_df[weather_df["month"].isin(months_to_consider)]
    avg_high_temp = filtered_weather["high temperature (°C)"].mean()
    avg_low_temp = filtered_weather["low temperature (°C)"].mean()
    avg_rainfall = filtered_weather["rainfall (mm)"].mean()
    avg_visitors_selected = avg_visitors[avg_visitors["Months"].isin(months_to_consider)]["average"].mean()

    # Rainfall comment
    if avg_rainfall < 20:
        rainfall_comment = "Rainfall is low, so weather should be mostly dry and pleasant."
    elif avg_rainfall < 100:
        rainfall_comment = "Rainfall is moderate, so occasional showers are possible."
    else:
        rainfall_comment = "High rainfall is expected, which may disrupt outdoor activities."

    # Temperature comment
    if avg_high_temp > 35:
        temp_comment = "Temperatures are high, which will be uncomfortable for most visitors. It is highly recommended to avoid this/these months."
    elif avg_high_temp < 20:
        temp_comment = "Temperatures are relatively cool and comfortable."
    else:
        temp_comment = "Temperatures are warm and generally comfortable."

    # Visitor comment
    if avg_visitors_selected > 100000:  # adjust threshold to your data scale
        visitor_comment = "Visitor numbers are high during these months, expect crowded sites."
    else:
        visitor_comment = "Visitor numbers are moderate, so it should be easier to enjoy the sites."

    # Combine dynamic conclusion
    conclusion = (
        f"For the selected months ({', '.join(months_to_consider)}): "
        f"{rainfall_comment} {temp_comment} {visitor_comment} "
        "These months provide a balanced experience for weather and tourism."
    )

    return conclusion

conclusion_text = get_conclusions(selected_months, weather_df, avg_visitors, month_order)

st.write(conclusion_text)











####### Allows the country to make money


# Line chart: tourism revenue in India over time

FEEs_tourism = pd.read_csv("datasets/FEEs_tourism.csv")

# Clean the 'FEEs in US $ Million' column by removing commas (if necessary) and converting to numeric
FEEs_tourism["FEEs in US $ Million"] = FEEs_tourism["FEEs in US $ Million"].replace(",", "", regex=True).astype(float)

# Filter only 'FEEs in US $ Million' data
fees_usd = FEEs_tourism[["Year", "FEEs in US $ Million"]]
fees_usd.rename(columns={"FEEs in US $ Million": "Revenue"}, inplace=True)

st.subheader("💰 Tourism Revenue in India (USD Millions) Over Time")




# Plot the filtered data for USD
chart = alt.Chart(fees_usd).mark_line(point=True).encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Revenue:Q", title="Tourism Revenue (USD Millions)"),
    tooltip=["Year", "Revenue"]
).properties(
    width=700,
    height=400,
    title="Tourism Revenue Growth in USD Millions (1991–2023)"
)

st.altair_chart(chart, use_container_width=True)

st.markdown("📈 **Post-COVID tourism revenue in USD** has shown strong recovery, reaching approximately **$28 billion** in 2023 — a significant increase of **31.5%** from 2022.")





###### estimates of how it helps the country

# Load and clean the data
GVA_GDP_df = pd.read_csv("datasets/GVA_GDP.csv")

# Fix column names
GVA_GDP_df.columns = [
    'Year', 'Total GVA', 'Total GDP',
    'Direct GVA', 'Direct GDP',
    'Direct GVA %', 'Direct GDP %',
    'GVA Multiplier',
    'Total GVA %', 'Total GDP %'
]

# Fix malformed value in Direct GVA
GVA_GDP_df['Direct GVA'] = GVA_GDP_df['Direct GVA'].replace('5,14,1,6', '5,14,116')

# Remove commas and convert relevant columns to float
cols_to_numeric = ['Total GVA', 'Total GDP', 'Direct GVA', 'Direct GDP']
for col in cols_to_numeric:
    GVA_GDP_df[col] = GVA_GDP_df[col].astype(str).str.replace(',', '').astype(float)

# Calculate Indirect GVA
GVA_GDP_df['Indirect GVA'] = GVA_GDP_df['Direct GVA'] * (GVA_GDP_df['GVA Multiplier'] - 1)

# Create the stacked area chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=GVA_GDP_df['Year'],
    y=GVA_GDP_df['Direct GVA'],
    name='Direct Tourism GVA',
    mode='lines',
    stackgroup='one',
    line=dict(width=0.5, color='#4CAF50')
))

fig.add_trace(go.Scatter(
    x=GVA_GDP_df['Year'],
    y=GVA_GDP_df['Indirect GVA'],
    name='Indirect Tourism GVA',
    mode='lines',
    stackgroup='one',
    line=dict(width=0.5, color='#81C784')
))

fig.update_layout(
    title='Tourism Contribution to GVA in India (Direct + Indirect)',
    xaxis_title='Year',
    yaxis_title='Gross Value Added (₹ Crore)',
    legend_title='Component',
    hovermode='x unified',
    template='plotly_white'
)

# Show in Streamlit
st.plotly_chart(fig)














# Timeline or calendar of major cultural festivals in these lesss popular regions









st.markdown("""
📌 **Best months to promote responsible tourism: February–March, October–November**. 
These months see a surge in international tourists, offering an ideal opportunity to focus on sustainable tourism practices.
By encouraging responsible travel during these peak times, we can ensure that tourism benefits local communities while preserving the environment.

Let’s strive for a balance between growth and sustainability, making tourism a force for good!
""")





#### Plan of actions resuming everything: flow chart showing to come in February–March, October–November to avoid tourists, rainfall and hot temperatures. showing the options of less visited cities and what you can do there.

