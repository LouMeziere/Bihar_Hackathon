# streamlit run main.py 



# main.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image
import streamlit.components.v1 as components
import re

st.title("🧭 Reimagining Tourism in Bihar: A Call for Responsible Travel")


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











airport_tourism = pd.read_csv("datasets/FTAs_airport.csv")
# Remove commas from 'FTAs' and convert to int
airport_tourism["FTAs"] = airport_tourism["FTAs"].str.replace(",", "").astype(int)

# Optional: Sort by FTAs for better visualization
airport_tourism = airport_tourism.sort_values(by="FTAs", ascending=False)

# Altair bar chart
chart = alt.Chart(airport_tourism).mark_bar().encode(
    x=alt.X("City:N", sort="-y"),
    y=alt.Y("FTAs:Q")
).properties(
    title="✈️ Airports Entry Points: Where Tourists Land in India",
    width=700,
    height=400
)

st.altair_chart(chart)








bihar_data = pd.DataFrame({
    "Year": [2000, 2001, 2002, 2003, 2004],
    "Domestic": [5.5, 6.1, 6.8, 7.4, 8.2],
    "Foreign": [110, 105, 95, 50, 38]  # In thousands
})

st.subheader("🛤️ Bihar: The Missed Opportunity")
st.line_chart(bihar_data.set_index("Year"))
st.markdown("- In 2023, Gaya Airport captured only **0.6%** of FTAs by air.")




col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌱 Environment", "Reduce Overtourism")
with col2:
    st.metric("💰 Economy", "Spread Tourism Income")
with col3:
    st.metric("🏛️ Culture", "Preserve Authenticity")



st.subheader("🌄 Why Bihar?")
st.markdown("""
- 🕉️ Bodh Gaya: UNESCO World Heritage Site
- 📉 Untapped potential in global tourism
- 👩‍🌾 Empower rural artisans and eco-guides
""")











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












st.subheader("📣 The Call to Action")
st.markdown("""
> Let’s **reimagine tourism** as mutual exchange. Bihar can become:
- 🐢 A model for **slow travel**
- 🧭 A beneficiary of **tourism decentralization**
- 🌾 A platform for **sustainability & local empowerment**
""")


