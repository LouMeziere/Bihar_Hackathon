# -------------------------------
#           Imports
# -------------------------------

import streamlit as st
import pandas as pd
import calendar
from utils.helpers import render_sidebar, load_table,  month_order
import streamlit.components.v1 as components
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px


from utils.helpers import inject_global_css

inject_global_css()


st.markdown(
    """
    <style>
    .app-container {
        max-width: 850px;
        margin: 20px auto;  /* centers horizontally, 20px vertical margin */
        padding: 0 10px;    /* optional horizontal padding */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------
#          Intro Section
# -------------------------------

# Display options of states and months in side bar
selected_states, selected_months = render_sidebar()

# Title & description
st.markdown("""
<div class="container" style="margin-top: 40px; margin-bottom: 0px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHEN </span>
  <span style="color: white; font-size: 53px; font-weight: 600;">the journey begins</span>
</div>
<div class="container" style="padding-top: 0px;">
    To help travelers make informed and responsible decisions, historical weather data (1991–2022), \
monthly visitor trends (2021–2023), and key local festivals were analyzed. This section highlights the best months to visit, so you can plan around weather, crowds, and cultural events.
</div>
""", unsafe_allow_html=True)










# ------------------------------
#     Ideal Weather Section
# -------------------------------

# --- Load & clean data ---
df_weather = load_table("weather_data")



# --- Line Plotting ---

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
        <div class=container>
            <h2 style="color:#ffffff; margin: 0 auto; max-width:850px;">Ideal Seasons for Perfect Weather</h2>
            <div style="
                font-size: 18px; 
                color: #93aca4; 
                line-height: 1.4; 
                font-family: Arial, sans-serif;
            ">
                From May through September, temperatures often soar, 
                with daytime heat reaching levels that may be uncomfortable for extended outdoor activities. This period also 
                marks the rainy season, bringing increased humidity and frequent showers that can impact travel plans and 
                outdoor excursions.
            </div>
        </div>
    """, unsafe_allow_html=True)


    # --- Weather Cards ---

    components.html(f"""
    <div style="max-width: 850px; margin: 0 auto;">
        <div style="display: flex; padding: 0 24px; gap: 20px; justify-content: space-between;">
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
        margin=dict(l=50, r=20, t=60, b=140),     # Chart margins
        height=500
    )   
    
    # Render the figure
    return fig

# plot_weather returns a Plotly fig
fig = plot_weather(selected_states)

# Set a fixed height in the figure layout for consistency
fig.update_layout(height=500)

left, center, right = st.columns([0.5, 8, 0.5])
with center:
    st.plotly_chart(fig, use_container_width=True)














# -------------------------------
#       Avoid Crowds Section
# -------------------------------

# Sub-title & description
st.markdown("""
<div class="container">
<h2 style="color:#ffffff; margin: 60px auto 20px auto;">Best Seasons to Escape the Crowds</h2>
<p>To enjoy a more peaceful and authentic experience while visiting India, it is best to avoid the busiest months of June, July, November, and December, when tourist arrivals peak and attractions become crowded. Planning your visit during the less crowded months of October, January, February, and March allows you to take advantage of pleasant weather while exploring popular destinations with fewer tourists. This approach not only enhances your travel experience but also promotes responsible tourism by helping to distribute visitor numbers more evenly throughout the year, easing pressure on local communities and the environment during peak seasons.</p>
</div>
""", unsafe_allow_html=True)




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

# Define years explicitly 
years = ['2023', '2022', '2021']

# Custom green color scale from dark green to flashy green
custom_colorscale = [
    [0.0, 'rgba(52, 244, 164, 1)'],   # flashy green
    [0.3, 'rgba(154, 250, 210, 1)'],  # text green (light)
    [0.6, 'rgba(28, 76, 84, 1)'],     # light green
    [1.0, 'rgba(4, 28, 28, 1)']      # dark green
]

# Prepare heatmap data: rows = years, columns = months
heatmap_data = df_visitors_month.set_index('months')[years].T

# Normalize data per year (row)
normalized_data = heatmap_data.copy()
for i, row in enumerate(normalized_data.values):
    min_val, max_val = row.min(), row.max()
    normalized_data.iloc[i] = (row - min_val) / (max_val - min_val)

# Prepare customdata as numpy array (absolute visitor numbers)
customdata = heatmap_data.values

# convert numpy array to list of lists
customdata_list = customdata.tolist()  

fig = go.Figure(
    go.Heatmap(
        z=normalized_data.values,
        x=month_order,
        y=years,
        colorscale=custom_colorscale,
        zmin=0,
        zmax=1,
        customdata=customdata_list,
        hovertemplate=(
            "Year: %{y}<br>"
            "Month: %{x}<br>"
            "Arrivals: %{customdata:.2f} M<br>"
            "<extra></extra>"
        ),
        colorbar=dict(
            title=dict(text='Normalized Arrivals', font=dict(color='#93aca4')),
            tickfont=dict(color='#93aca4'),
            outlinecolor='#282434',
            bordercolor='#282434'
        )
    )
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
    type='category'   # Forces y-axis to show only given categories            
)

# Enhance Heatmap Trace 
fig.update_traces(
    showscale=True,
    colorbar=dict(
        title=dict(text='Normalized<br>Arrivals', font=dict(color='#93aca4'), side='top'),
        tickfont=dict(color='#93aca4'),
        outlinecolor='#282434',
        bordercolor='#282434'
    )
)


left, center, right = st.columns([1, 8, 1])  # Wide center column

with center:
    st.plotly_chart(fig, use_container_width=True)  # Cleaner and responsive











# -------------------------------
#        Festivals Section
# -------------------------------

st.markdown(
    """
    <style>
    /* Page background and font */
   
    /* Responsive columns for cards */
    .stColumns > div {
        padding: 0 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sub-title
st.markdown("""
<div class="main">

<h2 style="color:#ffffff; max-width: 850px; text-align:left; font-weight: 900; font-size: 44px; margin: 30px auto 20px auto;">
    Plan Around India’s Festival Calendar
</h2>

<div style='color:#93aca4; max-width: 850px; padding-bottom:60px; margin: 0px auto;'>
    India’s calendar is rich with festivals — from Holi to regional music and dance celebrations. Choosing the right month can elevate your trip, offering a deeper cultural experience. Use this guide to discover when the biggest events take place this year.
</div>

</div>
""", unsafe_allow_html=True)




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

# --- Clamp month_index if needed ---
if "month_index" not in st.session_state:
    st.session_state.month_index = 0
else:
    # Clamp to available range
    st.session_state.month_index = min(
        st.session_state.month_index, max(0, len(available_months) - 1)
    )

# Optional: Reset index if current month no longer valid
if st.session_state.month_index >= len(available_months):
    st.session_state.month_index = 0


# Callback functions to update session state
def go_previous():
    if st.session_state.month_index > 0:
        st.session_state.month_index -= 1

def go_next():
    if st.session_state.month_index < len(available_months) - 1:
        st.session_state.month_index += 1




# --- Display Festival Cards for Selected Month ---

if available_months:
    # Retrieve selected month
    selected_year, selected_month = available_months[st.session_state.month_index]

    # Navigation buttons (Previous / Next)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.button("← Previous", on_click=go_previous)
    with col2:
        selected_year, selected_month = available_months[st.session_state.month_index]
        st.markdown(
            f"""
            <div style="display: flex; margin-top: -1.2rem; align-items: center; justify-content: center; height: 100%;">
                <h2 style='margin: 0;'>📅 Festivals in {calendar.month_name[selected_month]} {selected_year}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.button("Next →", on_click=go_next)


    # Filter festivals happening in the selected month
    this_month = grouped[
        (grouped["start_date"].dt.year == selected_year) &
        (grouped["start_date"].dt.month == selected_month)
    ].reset_index(drop=True)

    
    # Display festivals as cards, 2 per row
    cards_html = ""
    cards_per_row = 2

    for i in range(0, len(this_month), cards_per_row):
        row_html = "<div class='row' style='display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;'>"
        row = this_month.iloc[i : i + cards_per_row]

        for j in range(cards_per_row):
            if j < len(row):
                fest = row.iloc[j]
                start = fest["start_date"].date()
                end = fest["end_date"].date() if pd.notnull(fest["end_date"]) else None
                date_str = f"{start}" if not end or start == end else f"{start} → {end}"

                row_html += f"""
                    <div class="festival-card" style="flex: 1; background-color: #f7f7f7; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                        <h3 style="margin-top: 0;">{fest["festival_name"]}</h3>
                        <p><strong>📍 Location:</strong> {fest["city"]}, {fest["state"]}</p>
                        <p><strong>🎵 Genre:</strong> {fest["genre"]}</p>
                        <p><strong>📆 Date:</strong> {date_str}</p>
                        <details>
                            <summary>Details</summary>
                            <p>{fest["description"]}</p>
                        </details>
                    </div>
                """
            else:
                # Invisible placeholder to maintain layout when odd number of cards
                row_html += """
                    <div class="festival-card" style="flex: 1; visibility: hidden;"></div>
                """

        row_html += "</div>"
        cards_html += row_html


    # Full HTML with styling
    full_html = f"""
    <style>
    .container {{
        max-width: 870px;
        margin: 0 auto;
        padding: 20px;
    }}
    .row {{
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }}
    .festival-card {{
        flex: 1;
        background: linear-gradient(to bottom, #041c1c 11%, #1c4c54 90%, #041c1c 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 4px 4px 12px rgba(40, 36, 52, 0.8); /* subtle grey shadow */
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeIn 0.7s ease forwards;
        opacity: 0;
        max-width: 380px;            /* don't exceed main's width */
        width: 100%;  
        margin-left: auto;
        margin-right: auto;
    }}
    .festival-card h3 {{
        color: #ffffff;
        padding: 10px;
        border-radius: 6px;
        font-weight: 800;
    }}
    
    .festival-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }}
    /* Fade in keyframes */
    @keyframes fadeIn {{
        to {{ opacity: 1; }}
    }}
    
    .festival-card p {{
        color: #93aca4 ;
    }}
    /* Details summary styling */
    details summary {{
        cursor: pointer;
        font-weight: 600;
        color: #34f4a4 ;
        outline: none;
        margin-top: 1rem;
    }}
    details[open] summary::after {{
        content: "▲";
        float: right;
    }}
    details summary::after {{
        content: "▼";
        float: right;
    }}
    details p {{
        margin-top: 0.5rem;
        color: #93aca4 ;
        font-size: 0.95rem;
        line-height: 1.3;
    }}

    </style>
    <div class="container">
        {cards_html}
    </div>
    """

    # Render in component
    components.html(full_html, height=700, scrolling=True)

else:
    # Message when no festivals are available
    st.markdown(
        """
        <div style='
            background: linear-gradient(to right, #041c1c 0%, #1c4c54 50%, #041c1c 100%);
            color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            margin: 30px auto;
            max-width: 600px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(6px);
        '>
            🚫 No festival data available.
        </div>
        """,
        unsafe_allow_html=True
    )



st.markdown('</div>', unsafe_allow_html=True)