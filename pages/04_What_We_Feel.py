
import streamlit as st
import pandas as pd
import altair as alt
from utils.helpers import render_sidebar

selected_states, selected_months = render_sidebar()

st.subheader("📅 When to Visit: Monthly Travel Trends & Insights")
st.markdown("""
To help travelers make informed and responsible choices, we analyzed **historical weather data (1991–2022)** alongside **monthly visitor trends (2021–2023)**.  
This allows us to identify months that offer **comfortable weather** while avoiding overcrowded periods — promoting a more **sustainable and enjoyable travel experience**.

""")

# Load data
monthwise_ITAs = pd.read_csv("datasets/monthwise_ITAs.csv")
df_weather = pd.read_csv("datasets/weather_data.csv")
months = df_weather['month'].dropna().unique()

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
