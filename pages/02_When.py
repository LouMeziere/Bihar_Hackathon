# -------------------------------
#           Imports
# -------------------------------

import streamlit as st
import pandas as pd
import calendar
from utils.helpers import render_sidebar, load_table,  month_order
import streamlit.components.v1 as components

import plotly.graph_objects as go
import plotly.express as px





# -------------------------------
#          Intro Section
# -------------------------------

# Display options of states and months in side bar
selected_states, selected_months = render_sidebar()

# Title
st.markdown("""
<div style="text-align: left; margin-top: 40px; margin-bottom: 40px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHEN </span>
  <span style="color: white; font-size: 53px; font-weight: 600;">the journey begins</span>
</div>
""", unsafe_allow_html=True)

# Intro paragraph
st.markdown("")

st.markdown("""
<div style='color:#ffffff;'>
    To help travelers make informed and responsible decisions, historical weather data (1991–2022)" \
", monthly visitor trends (2021–2023), and key local festivals were analyzed. This section highlights the best months to visit, so you can plan around weather, crowds, and cultural events.
</div>
""", unsafe_allow_html=True)

# Sub-title 
st.markdown("""
<h2 style="color:#ffffff; text-align:left; font-weight: 900; font-size: 44px; margin: 70px 0 20px 0;">Ideal Seasons for Perfect Weather</h2>
""", unsafe_allow_html=True)




# -------------------------------
#     Ideal Weather Section
# -------------------------------

# --- Load & clean data ---
df_weather = load_table("weather_data")



# --- Plotting ---

def plot_weather(selected_states):
    # Check if any states have been selected by the user
    if not selected_states:
        # No states selected: use the full weather dataset
        df_weather_filtered = df_weather.copy()
        title = "Average Weather Across All States"
    else:
        # Filter the dataset to include only the selected states
        df_weather_filtered = df_weather[df_weather['state'].isin(selected_states)]

        # Set title depending on how many states are selected
        if len(selected_states) == 1:
            title = f"Weather Data for {selected_states[0]}"
        else:
            title = f"Average Weather for Selected States: {', '.join(selected_states)}"

    # Group the filtered data by month and calculate mean and standard deviation of average temperature
    # Reindex by the predefined month_order list to ensure months are in correct calendar order
    agg = df_weather_filtered.groupby('month')['avg_temperature_c'].agg(['mean', 'std']).reindex(month_order)

    # Calculate May to September stats
    hot_months = ['May', 'June', 'July', 'August', 'September']
    hot_data = df_weather_filtered[df_weather_filtered['month'].isin(hot_months)]

    avg_min_temp = hot_data['min_temperature_c'].mean()
    avg_max_temp = hot_data['max_temperature_c'].mean()
    avg_rainfall = hot_data['rainfall_mm'].mean()

    # Explanation text above cards (no background)
    st.markdown("""
        <div style="
            font-size: 18px; 
            color: #93aca4; 
            line-height: 1.4; 
            margin-bottom: 20px;
            font-family: Arial, sans-serif;
        ">
            From May through September, temperatures often soar, 
            with daytime heat reaching levels that may be uncomfortable for extended outdoor activities. This period also 
            marks the rainy season, bringing increased humidity and frequent showers that can impact travel plans and 
            outdoor excursions.
        </div>
    """, unsafe_allow_html=True)


    # --- Weather Cards ---

    components.html(f"""
        <div style="display: flex; gap: 20px; justify-content: space-between;">
            <div style="
                flex: 1;
                background: linear-gradient(to right, #1e2f2f, #1c4c54);
                padding: 15px; 
                border-radius: 10px; 
                color: #34f4a4;
                font-weight: 700;
                font-family: Arial, sans-serif;
                text-align: center;
            ">
                <div style="font-size:14px; margin-bottom:4px; color: #93aca4;">Avoid High Temp</div>
                <div style="font-size: 40px; font-weight: 900;">{avg_min_temp:.1f} – {avg_max_temp:.1f}°C</div>
                <div style="font-size:12px; color:#ffffff; margin-top:4px;">🌡️ May–Sep avg.</div>
            </div>

            <div style="
                flex: 1;
                background: linear-gradient(to right, #1c4c54, #1e2f2f);
                padding: 15px; 
                border-radius: 10px; 
                color: #34f4a4;
                font-weight: 700;
                font-family: Arial, sans-serif;
                text-align: center;
            ">
                <div style="font-size:14px; margin-bottom:4px; color: #93aca4;">Avoid Rainfall</div>
                <div style="font-size: 40px; font-weight: 900;">{avg_rainfall:.1f} mm</div>
                <div style="font-size:12px; color:#ffffff; margin-top:4px;">☔ May–Sep avg.</div>
            </div>
        </div>
    """, height=180)



    # --- Plot ---

    # Create a new Plotly figure
    fig = go.Figure()

    # Add a line plot for average temperature with markers
    fig.add_trace(go.Scatter(
        x=agg.index,                        # Months on x-axis
        y=agg['mean'],                      # Mean temperatures on y-axis
        mode='lines+markers',              # Show both lines and markers
        line=dict(color='#34f4a4'),        # Line color
        marker=dict(size=6),               # Marker size
        name='Avg Temp',                   # Legend label
        hovertemplate='Month: %{x}<br>Temperature: %{y:.1f} ± %{customdata:.1f} °C',  # Hover info
        customdata=agg['std'].values.reshape(-1, 1)  # Standard deviation for hover display
    ))

    # Add a shaded area to represent one standard deviation around the mean
    fig.add_trace(go.Scatter(
        x=agg.index.tolist() + agg.index[::-1].tolist(),  # Combine x-axis for upper and lower bounds
        y=(agg['mean'] + agg['std']).tolist() + (agg['mean'] - agg['std'])[::-1].tolist(),  # Upper + lower bound
        fill='toself',                        # Fill the area between curves
        fillcolor='rgba(147, 172, 164, 0.15)',# Light fill color
        line=dict(color='rgba(255,255,255,0)'), # Invisible border
        hoverinfo="skip",                     # Skip hover for this trace
        name='Std Dev'                        # Legend label
    ))

    # Update layout and styling for dark theme and custom colors
    fig.update_layout(
        plot_bgcolor='#101414',               # Dark plot background
        paper_bgcolor='#101414',              # Dark overall background
        title=dict(
            text=title,                       # Title based on selected states
            font=dict(color='#9ee0cc', size=18, family='Arial'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(                           # X-axis formatting
            title=dict(text='Month', font=dict(color='#93aca4')),
            tickfont=dict(color='#9ee0cc'),
            showgrid=True,
            gridcolor='#2a3a3a',
            showline=True,
            linecolor='#93aca4',
            linewidth=1.1,
            showticklabels=True,
            ticks='outside',
            tickcolor='#9ee0cc',
            tickwidth=1.1,
            ticklen=8,
        ),
        yaxis=dict(                           # Y-axis formatting
            title=dict(text='Average Temperature (°C)', font=dict(color='#93aca4')),
            tickfont=dict(color='#9ee0cc'),
            showgrid=True,
            gridcolor='#2a3a3a',
            showline=True,
            linecolor='#93aca4',
            linewidth=1.1,
            showticklabels=True,
            ticks='outside',
            tickcolor='#9ee0cc',
            tickwidth=1.1,
            ticklen=8,
        ),
        legend=dict(font=dict(color='#93aca4')),  # Legend font color
        margin=dict(l=40, r=20, t=60, b=40)       # Chart margins
    )

    # Render the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Assuming selected_states is defined, or pass an empty list if none selected
plot_weather(selected_states)















# -------------------------------
#       Avoid Crowds Section
# -------------------------------

# Sub-title
st.markdown("""
<h2 style="color:#ffffff; text-align:left; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Best Seasons to Escape the Crowds</h2>
""", unsafe_allow_html=True)

# Description
st.markdown("""
To enjoy a more peaceful and authentic experience while visiting India, it is best to avoid the busiest months of June, July, November, and December, when tourist arrivals peak and attractions become crowded. Planning your visit during the less crowded months of October, January, February, and March allows you to take advantage of pleasant weather while exploring popular destinations with fewer tourists. This approach not only enhances your travel experience but also promotes responsible tourism by helping to distribute visitor numbers more evenly throughout the year, easing pressure on local communities and the environment during peak seasons.
""")


# --- Load & clean data ---

df_visitors_month = load_table("monthwise_ITAs")

# Drop null values
df_visitors_month = df_visitors_month.dropna(how='all')

# Change columns that start with _ to remove char
df_visitors_month.columns = [col[1:] if col.startswith('_') and col[1:].isdigit() else col for col in df_visitors_month.columns]

# Convert the 'months' column to a categorical type with a defined order
df_visitors_month['months'] = pd.Categorical(df_visitors_month['months'], categories=month_order, ordered=True)

# Convert visitor numbers to millions for better readability
for col in ['2021', '2022', '2023']:
    df_visitors_month[col] = df_visitors_month[col] / 1_000_000

# Prepare data for heatmap: years as rows, months as columns
heatmap_data = df_visitors_month.set_index('months')[['2021', '2022', '2023']].T



# --- Plot ---

# Custom green color scale from dark green to flashy green
custom_colorscale = [
    [0.0, 'rgba(4, 28, 28, 1)'],      # dark green
    [0.3, 'rgba(28, 76, 84, 1)'],     # light green
    [0.6, 'rgba(147, 172, 164, 1)'],  # text green (light)
    [1.0, 'rgba(52, 244, 164, 1)']    # flashy green
]

# Create Heatmap
fig = px.imshow(
    heatmap_data,  # Data in matrix format (years as rows, months as columns)
    labels=dict(x="Month", y="Year", color="Tourist Arrivals"),  
    x=month_order,  # Explicit month order for x-axis
    y=['2021', '2022', '2023'], 
    color_continuous_scale=custom_colorscale,  
    aspect="auto",  
)

# General Layout Customization 
fig.update_layout(
    plot_bgcolor='#101414',      
    paper_bgcolor='#101414',      
    font=dict(color='#93aca4', family="Arial, sans-serif"),  
    title=dict(
        text="Monthly Tourist Arrivals Heatmap",  
        font=dict(size=24, color='#ffffff'),     
        x=0.5,                                     
        xanchor='center',
    ),
    margin=dict(t=60, l=50, r=50, b=50),  # Margins around the chart
)

# Customize X-axis Appearance
fig.update_xaxes(
    showgrid=False,                  # Remove gridlines
    tickangle=45,                   # Tilt x-axis labels for readability
    tickfont=dict(color='#93aca4'), 
    linecolor='#282434',            
    zeroline=False,                 # Hide baseline at 0
)

# Customize Y-axis Appearance
fig.update_yaxes(
    showgrid=False,                  
    tickfont=dict(color='#93aca4'),
    linecolor='#282434',            
    zeroline=False,                 
)

# Enhance Heatmap Trace 
fig.update_traces(
    hovertemplate='Year: %{y}<br>Month: %{x}<br>Arrivals: %{z:.2f} M <extra></extra>',  # Custom tooltip
    showscale=True,  # Show color bar
    colorbar=dict(   # Style the color bar
        title=dict(
            text='Arrivals',
            font=dict(color='#93aca4')
        ),
        tickfont=dict(color='#93aca4'),
        outlinecolor='#282434',  # Color bar border color
        bordercolor='#282434',
    )
)

# Display the Chart in Streamlit 
st.plotly_chart(fig, use_container_width=True)













# -------------------------------
#        Festivals Section
# -------------------------------

# Sub-title
st.markdown("""
<h2 style="color:#fffff; text-align:left; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Plan Around India’s Festival Calendar</h2>
""", unsafe_allow_html=True)

# Description
st.markdown("""
<div style='color:#93aca4; padding-bottom:30px;'>
   India’s calendar is rich with festivals — from Holi to regional music and dance celebrations. Choosing the right month can elevate your trip, offering a deeper cultural experience. Use this guide to discover when the biggest events take place this year.
</div>
""", unsafe_allow_html=True)



st.markdown(
    """
    <style>
    /* Page background and font */
    .main {
        background-color: #f9f9f9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #222222;
    }
    /* Container for festival cards */
    .festival-card {
        background: linear-gradient(to bottom, #041c1c 11%, #1c4c54 90%, #041c1c 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 4px 4px 12px rgba(40, 36, 52, 0.8); /* subtle grey shadow */
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeIn 0.7s ease forwards;
        opacity: 0;
    
    }
    .festival-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    /* Fade in keyframes */
    @keyframes fadeIn {
        to { opacity: 1; }
    }
    /* Headers */
    h1, h2, h3 {
        font-weight: 700;
        color: #1c4c54;
        margin-bottom: 0.3rem;
    }
    h1 {
        font-size: 2.5rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    h2 {
        font-size: 1.8rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.4rem;
    }
    .festival-card p {
        color: #93aca4 ;
    }
    /* Details summary styling */
    details summary {
        cursor: pointer;
        font-weight: 600;
        color: #34f4a4 ;
        outline: none;
        margin-top: 1rem;
    }
    details[open] summary::after {
        content: "▲";
        float: right;
    }
    details summary::after {
        content: "▼";
        float: right;
    }
    details p {
        margin-top: 0.5rem;
        color: #93aca4 ;
        font-size: 0.95rem;
        line-height: 1.3;
    }
    /* Responsive columns for cards */
    .stColumns > div {
        padding: 0 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Load & clean data ---

df_festival = load_table("festivals_data")

# Remove rows where state information is missing
df_festival = df_festival.dropna(subset=['state'])

# Convert start and end dates to datetime, filtering out parsing errors
df_festival["start_date"] = pd.to_datetime(df_festival["start_date"], format='%d %b %Y', errors="coerce")
df_festival["end_date"] = pd.to_datetime(df_festival["end_date"], format='%d %b %Y', errors="coerce")

# Keep only future festivals (starting from May 2025)
df_festival = df_festival[(df_festival["start_date"].dt.year >= 2025) & (df_festival["start_date"].dt.month >= 5)]



# --- Filtering Based on User Selections ---

filtered_festivals = df_festival.copy()

# Filter festivals by selected states
if selected_states:
    filtered_festivals = filtered_festivals[filtered_festivals["state"].isin(selected_states)]

# Filter festivals by selected months (converted from month names to numbers)
if selected_months:
    month_number_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    selected_month_nums = [month_number_map[m] for m in selected_months]
    filtered_festivals = filtered_festivals[
        filtered_festivals["start_date"].dt.month.isin(selected_month_nums)
    ]



# --- Grouping Festival Info for Display ---

# Group by festival info and combine multiple states into comma-separated strings
grouped = (
    filtered_festivals
    .groupby(["festival_name", "start_date", "end_date", "description", "genre", "city"], dropna=False)
    .agg({"state": lambda x: ", ".join(sorted(set(x.dropna())))})
    .reset_index()
)

# Sort festivals chronologically
grouped = grouped.sort_values(by="start_date")

# Get list of unique (year, month) tuples for available festivals
available_months = sorted(grouped["start_date"].dropna().apply(lambda d: (d.year, d.month)).unique())



# --- Month Navigation Logic ---

# Initialize session state to keep track of current month index
if "month_index" not in st.session_state:
    st.session_state.month_index = 0



# --- Display Festival Cards for Selected Month ---

if available_months:
    # Retrieve selected month
    selected_year, selected_month = available_months[st.session_state.month_index]

    # Navigation buttons (Previous / Next)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Previous"):
            if st.session_state.month_index > 0:
                st.session_state.month_index -= 1
    with col2:
        st.markdown(
            f"""
            <div style="display: flex; margin-top: -1.2rem; margin-bottom: 30px; align-items: center; justify-content: center; height: 100%;">
                <h2 style='margin: 0;'>📅 Festivals in {calendar.month_name[selected_month]} {selected_year}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        if st.button("Next →"):
            if st.session_state.month_index < len(available_months) - 1:
                st.session_state.month_index += 1

    # Filter festivals happening in the selected month
    this_month = grouped[
        (grouped["start_date"].dt.year == selected_year) &
        (grouped["start_date"].dt.month == selected_month)
    ].reset_index(drop=True)

    # Display festivals as cards, 2 per row
    cards_per_row = 2
    for i in range(0, len(this_month), cards_per_row):
        row_festivals = this_month.iloc[i : i + cards_per_row]
        cols = st.columns(cards_per_row)
        for col, (_, row) in zip(cols, row_festivals.iterrows()):
            with col:
                start = row['start_date'].date()
                end = row['end_date'].date() if pd.notnull(row['end_date']) else None
                date_str = f"{start}" if not end or start == end else f"{start} → {end}"

                # Render a styled card for each festival
                st.markdown(
                    f"""
                    <div class="festival-card">
                        <h3 style='color:#ffffff; font-weight:800; margin-bottom:20px;'>{row['festival_name']}</h3>
                        <p><strong style='color:#041c1c;font-weight:800;'>📍 Location:</strong> {row['city']}, {row['state']}</p>
                        <p><strong style='color:#041c1c;font-weight:800;'>🎵 Genre:</strong> {row['genre']}</p>
                        <p><strong style='color:#041c1c;font-weight:800;'>📆 Date:</strong> {date_str}</p>
                        <details>
                            <summary>Details</summary>
                            <p>{row['description']}</p>
                        </details>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
else:
    # Message when no festivals are available
    st.info("No festival data available.")