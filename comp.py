import streamlit as st
import pandas as pd
import numpy as np
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
        placeholder="All Months"
    )

# --- 5. Apply Filters ---
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
    html = f"""
    <div style="width:220px">
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
st_data = st_folium(m, width=800, height=600)







# --- 7. Top 3 Most Visited Monuments (Filtered) ---
st.subheader("🏆 Top 3 Most Visited Monuments (2023-24)")

# Sort and select top 3 from filtered data
top_3_monuments = filtered_df.sort_values('2023-24 total visitors', ascending=False).head(3)

for _, row in top_3_monuments.iterrows():
    col1, col2 = st.columns([1, 2])
    with col1:
        # Check if image URL exists
        if pd.notna(row.get('image_url')):
            st.image(row['image_url'], width=150, caption=row['monument'])
        else:
            st.markdown("🖼️ *No image available*")
    with col2:
        st.markdown(f"**{row['monument']}**")
        st.markdown(f"📍 {row['city']}, {row['state']}")
        st.markdown(f"👥 **{row['2023-24 total visitors']:,} visitors**")
        st.markdown(f"📈 Domestic Growth: {row['% domestic growth']}%")
    st.markdown("---")






# --- Load and prepare data ---
weather_df = pd.read_csv("datasets/patna_weather.csv")

# Define month orders
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
month_abbr_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_abbr_map = dict(zip(month_order, month_abbr_order))

# Prepare columns
weather_df["month"] = pd.Categorical(weather_df["month"], categories=month_order, ordered=True)
weather_df = weather_df.sort_values("month").reset_index(drop=True)
weather_df["month_abbr"] = weather_df["month"].map(month_abbr_map)

# --- Prepare temperature data ---
gradient_df = weather_df[["month_abbr", "high temperature (°C)", "low temperature (°C)"]].copy()
gradient_df.rename(columns={"high temperature (°C)": "high", "low temperature (°C)": "low"}, inplace=True)
gradient_df["month_abbr"] = pd.Categorical(gradient_df["month_abbr"], categories=month_abbr_order, ordered=True)
gradient_df = gradient_df.sort_values("month_abbr").reset_index(drop=True)

# Melt data for temperature lines
line_df = pd.melt(
    gradient_df,
    id_vars="month_abbr",
    value_vars=["high", "low"],
    var_name="Temperature Type",
    value_name="Value"
)

# --- Prepare rainfall data ---
rainfall_df = weather_df[["month_abbr", "rainfall (mm)"]].copy()
rainfall_df["month_abbr"] = pd.Categorical(rainfall_df["month_abbr"], categories=month_abbr_order, ordered=True)
rainfall_df = rainfall_df.sort_values("month_abbr").reset_index(drop=True)

# --- Create charts ---

# Rainfall area (secondary axis)
rainfall_area = alt.Chart(rainfall_df).mark_area(
    opacity=0.2,
    color="#1f77b4"
).encode(
    x=alt.X("month_abbr:N", sort=month_abbr_order, title="Month"),
    y=alt.Y("rainfall (mm):Q", axis=alt.Axis(title="Rainfall (mm)", titleColor="#1f77b4"))
)

# Temperature area between high and low
area = alt.Chart(gradient_df).mark_area(
    interpolate='linear',
    opacity=0.3
).encode(
    x=alt.X("month_abbr:N", title="Month", sort=month_abbr_order),
    y=alt.Y("low:Q", scale=alt.Scale(domain=[10, 45]), axis=alt.Axis(title="Temperature (°C)", titleColor="#FF5733")),
    y2=alt.Y2("high:Q"),
    tooltip=["month_abbr", "low", "high"]
)

# Line colors
line_colors = alt.Scale(domain=["high", "low"], range=["#FF5733", "#1F77B4"])

# Temperature lines
lines = alt.Chart(line_df).mark_line(point=True).encode(
    x=alt.X("month_abbr:N", sort=month_abbr_order),
    y=alt.Y("Value:Q"),
    color=alt.Color("Temperature Type:N", scale=line_colors),
    tooltip=["month_abbr", "Temperature Type", "Value"]
)

# Combine all
combined_chart = alt.layer(
    rainfall_area,
    area,
    lines
).resolve_scale(
    y='independent'
).properties(
    title="Monthly Temperatures and Rainfall in Patna",
    width=700,
    height=400
)

# --- Streamlit Display ---
st.title("📊 Climate Overview of Patna")

st.subheader("Combined Temperature and Rainfall Chart")
st.write("**Best time to visit Patna** is from **October to April** with comfortable temperatures and minimal rainfall.")
st.altair_chart(combined_chart, use_container_width=True)

# Optional: Extra insights or notes
st.caption("Rainfall peaks during July and August. Plan your travel accordingly to avoid monsoon disruptions.")











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







"""2. Promote Responsible Tourism"""

###### Choose to visit less visited states. Better experience for yourself as less crowded. also, it doesnt mean they are less dense in culture

# Load dataset
df = pd.read_csv("datasets/cultural_sites.csv", encoding="windows-1252")

# Group by state to calculate total visitors and number of sites
grouped = df.groupby("state").agg({
    "2023-24 total visitors": "sum",
    "monument": "count"  # Assuming this column is the site name
}).rename(columns={"2023-24 total visitors": "Total Visitors", "monument": "Number of Sites"})

# Calculate visitors per site
grouped["Visitors per Site"] = grouped["Total Visitors"] / grouped["Number of Sites"]

# Sort to find under-visited culturally rich states
under_visited = grouped.sort_values("Visitors per Site").head(10)

# Reset index so 'state' becomes a column
under_visited = under_visited.reset_index()

# Create a better-looking bar chart
fig = px.bar(
    under_visited,
    x="state",
    y="Visitors per Site",
    title="Top 10 Under-Visited but Culturally Rich States",
    labels={"state": "State", "Visitors per Site": "Avg Visitors per Site"},
    color="Visitors per Site",
    color_continuous_scale="Tealgrn"
)

# Update layout for cleaner look
fig.update_layout(
    xaxis=dict(categoryorder="total ascending"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#333", size=14),
    title_font=dict(size=18),
    margin=dict(t=60, b=40, l=20, r=20)
)

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add interpretation text
st.markdown(
    """
    These states have multiple cultural sites, yet receive relatively fewer visitors per site.
    This may indicate opportunities for responsible tourism development and awareness campaigns.
    """
)








# Timeline or calendar of major cultural festivals in these lesss popular regions









###### Show when tourists tend to come to india to avoid the most busy months

# Load the monthwise ITAs data
monthwise_ITAs = pd.read_csv("datasets/monthwise_ITAs.csv")

# Remove commas from the data and convert to integers
monthwise_ITAs["2021"] = monthwise_ITAs["2021"].replace(",", "", regex=True)
monthwise_ITAs["2022"] = monthwise_ITAs["2022"].replace(",", "", regex=True)
monthwise_ITAs["2023"] = monthwise_ITAs["2023"].replace(",", "", regex=True)

# Convert columns to numeric, handling errors that may arise (like unexpected characters)
monthwise_ITAs["2021"] = pd.to_numeric(monthwise_ITAs["2021"], errors="coerce")
monthwise_ITAs["2022"] = pd.to_numeric(monthwise_ITAs["2022"], errors="coerce")
monthwise_ITAs["2023"] = pd.to_numeric(monthwise_ITAs["2023"], errors="coerce")

# If there are any NaNs, fill them with 0 (or another appropriate value)
monthwise_ITAs["2021"].fillna(0, inplace=True)
monthwise_ITAs["2022"].fillna(0, inplace=True)
monthwise_ITAs["2023"].fillna(0, inplace=True)

# Reshape the data to have one column for year and one column for ITAs
monthwise_ITAs_melted = monthwise_ITAs.melt(id_vars=["Months"], 
                                            value_vars=["2021", "2022", "2023"],
                                            var_name="Year", 
                                            value_name="ITAs")

# Remove rows where ITAs is NaN or zero
monthwise_ITAs_melted = monthwise_ITAs_melted[monthwise_ITAs_melted["ITAs"] > 0]

# Define the month order for proper sorting
month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]

# Create the line chart
chart = alt.Chart(monthwise_ITAs_melted).mark_line(point=True).encode(
    x=alt.X("Months:N", title="Month", sort=month_order),  # Sort months in natural order
    y=alt.Y("ITAs:Q", title="International Tourist Arrivals (ITAs)"),
    color="Year:N",  # Color by Year
    tooltip=["Months", "ITAs", "Year"]
).properties(
    width=700,
    height=400,
    title="Monthly International Tourist Arrivals (ITAs) in India (2021–2023)"
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)

st.markdown("""
📌 **Best months to promote responsible tourism: February–March, October–November**. 
These months see a surge in international tourists, offering an ideal opportunity to focus on sustainable tourism practices.
By encouraging responsible travel during these peak times, we can ensure that tourism benefits local communities while preserving the environment.

Let’s strive for a balance between growth and sustainability, making tourism a force for good!
""")





#### Plan of actions resuming everything: flow chart showing to come in February–March, October–November to avoid tourists, rainfall and hot temperatures. showing the options of less visited cities and what you can do there.

