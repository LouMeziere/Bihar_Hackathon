
import streamlit as st
import pandas as pd
import altair as alt
import calendar
from utils.helpers import render_sidebar
import streamlit.components.v1 as components

selected_states, selected_months = render_sidebar()

st.markdown("""
<div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHEN </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">the journey begins</span>
</div>
""", unsafe_allow_html=True)

st.markdown("To help travelers make informed and responsible decisions, we've analyzed historical weather data (1991–2022)" \
", monthly visitor trends (2021–2023), and key local festivals. This section highlights the best months to visit, so you can plan around weather, crowds, and cultural events.")


st.markdown("""
<h2 style="color:#fffff; text-align:left; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Ideal Seasons for Perfect Weather</h2>
""", unsafe_allow_html=True)


import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

@st.cache_data
def load_data():
    return pd.read_csv('datasets/weather_data.csv')

df = load_data()

def plot_weather(selected_states):
    if not selected_states:
        df_filtered = df.copy()
        title = "Average Weather Across All States"
    else:
        df_filtered = df[df['state'].isin(selected_states)]
        if len(selected_states) == 1:
            title = f"Weather Data for {selected_states[0]}"
        else:
            title = f"Average Weather for Selected States: {', '.join(selected_states)}"

    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    agg = df_filtered.groupby('month')['Avg. Temperature (°C)'].agg(['mean', 'std']).reindex(month_order)

    # Calculate May to September stats
    hot_months = ['May', 'June', 'July', 'August', 'September']
    hot_data = df_filtered[df_filtered['month'].isin(hot_months)]

    avg_min_temp = hot_data['Min Temperature (°C)'].mean()
    avg_max_temp = hot_data['Max Temperature (°C)'].mean()
    avg_rainfall = hot_data['Rainfall (mm)'].mean()

    # Explanation text above cards (no background)
    st.markdown("""
        <div style="
            font-size: 18px; 
            color: #f0f0f0; 
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

    # Two cards side-by-side for the stats
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
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=agg.index,
        y=agg['mean'],
        mode='lines+markers',
        line=dict(color='#34f4a4'),
        marker=dict(size=6),
        name='Avg Temp',
        hovertemplate='Month: %{x}<br>Temperature: %{y:.1f} ± %{customdata:.1f} °C',
        customdata=agg['std'].values.reshape(-1, 1)
    ))

    fig.add_trace(go.Scatter(
        x=agg.index.tolist() + agg.index[::-1].tolist(),
        y=(agg['mean'] + agg['std']).tolist() + (agg['mean'] - agg['std'])[::-1].tolist(),
        fill='toself',
        fillcolor='rgba(147, 172, 164, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        name='Std Dev'
    ))

    fig.update_layout(
        plot_bgcolor='#101414',
        paper_bgcolor='#101414',
        title=dict(
            text=title,
            font=dict(color='#9ee0cc', size=18, family='Arial'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
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
        yaxis=dict(
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
        legend=dict(font=dict(color='#93aca4')),
        margin=dict(l=40, r=20, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


# Assuming selected_states is defined, or pass an empty list if none selected
plot_weather(selected_states)
















st.markdown("""
<h2 style="color:#fffff; text-align:left; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Best Seasons to Escape the Crowds</h2>
""", unsafe_allow_html=True)

st.markdown("""
To enjoy a more peaceful and authentic experience while visiting India, it is best to avoid the busiest months of June, July, November, and December, when tourist arrivals peak and attractions become crowded. Planning your visit during the less crowded months of October, January, February, and March allows you to take advantage of pleasant weather while exploring popular destinations with fewer tourists. This approach not only enhances your travel experience but also promotes responsible tourism by helping to distribute visitor numbers more evenly throughout the year, easing pressure on local communities and the environment during peak seasons.
""")


import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
monthwise_ITAs = pd.read_csv("datasets/monthwise_ITAs.csv")
# Drop any rows where all columns except maybe 'Months' are empty or NaN
monthwise_ITAs = monthwise_ITAs.dropna(how='all')

# Remove commas and convert numbers (for columns '2021', '2022', '2023')
for col in ['2021', '2022', '2023']:
    monthwise_ITAs[col] = monthwise_ITAs[col].astype(str).str.replace(',', '').astype(float)

# Order months
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
monthwise_ITAs['Months'] = pd.Categorical(monthwise_ITAs['Months'], categories=month_order, ordered=True)
monthwise_ITAs = monthwise_ITAs.sort_values('Months')

# Prepare data for heatmap: years as rows, months as columns
heatmap_data = monthwise_ITAs.set_index('Months')[['2021', '2022', '2023']].T

import plotly.express as px
import streamlit as st

# Your data loading and cleaning code goes here (as you wrote)...

# Custom green color scale from dark green to flashy green
custom_colorscale = [
    [0.0, 'rgba(4, 28, 28, 1)'],      # dark green
    [0.3, 'rgba(28, 76, 84, 1)'],     # light green
    [0.6, 'rgba(147, 172, 164, 1)'],  # text green (light)
    [1.0, 'rgba(52, 244, 164, 1)']    # flashy green
]

fig = px.imshow(
    heatmap_data,
    labels=dict(x="Month", y="Year", color="Tourist Arrivals"),
    x=month_order,
    y=['2021', '2022', '2023'],
    color_continuous_scale=custom_colorscale,
    aspect="auto",
)

fig.update_layout(
    plot_bgcolor='#101414',       # your background color
    paper_bgcolor='#101414',
    font=dict(color='#93aca4', family="Arial, sans-serif"),  # light green text color & font
    title=dict(
        text="Monthly Tourist Arrivals Heatmap",
        font=dict(size=24, color='#ffffff'),
        x=0.5,
        xanchor='center',
    ),
    margin=dict(t=60, l=50, r=50, b=50),
)

fig.update_xaxes(
    showgrid=False,
    tickangle=45,
    tickfont=dict(color='#93aca4'),
    linecolor='#282434',           # grey axis lines
    zeroline=False,
)

fig.update_yaxes(
    showgrid=False,
    tickfont=dict(color='#93aca4'),
    linecolor='#282434',           # grey axis lines
    zeroline=False,
)

# Add subtle white border around heatmap cells for clarity
fig.update_traces(
    hovertemplate='Year: %{y}<br>Month: %{x}<br>Arrivals: %{z}<extra></extra>',
    showscale=True,
    colorbar=dict(
        title=dict(
            text='Arrivals',
            font=dict(color='#93aca4')
        ),
        tickfont=dict(color='#93aca4'),
        outlinecolor='#282434',
        bordercolor='#282434',
    )
)


st.plotly_chart(fig, use_container_width=True)















st.markdown("""
<h2 style="color:#fffff; text-align:left; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Timing Your Trip Around India’s Grand Celebrations</h2>
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
        background: linear-gradient(to bottom, #041c1c 0%, #1c4c54 50%, #041c1c 100%);
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
        margin-bottom: 1.2rem;
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

# Your existing data loading and filtering code remains unchanged:
df_festival = pd.read_csv("datasets/festivals_data.csv", encoding='utf-8')
df_festival = df_festival.dropna(subset=['state'])
df_festival["start_date"] = pd.to_datetime(df_festival["start_date"], format='%d %b %Y', errors="coerce")
df_festival["end_date"] = pd.to_datetime(df_festival["end_date"], format='%d %b %Y', errors="coerce")
df_festival = df_festival[(df_festival["start_date"].dt.year >= 2025) & (df_festival["start_date"].dt.month >= 5)]

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
        filtered_festivals["start_date"].dt.month.isin(selected_month_nums)
    ]

grouped = (
    filtered_festivals
    .groupby(["festival_name", "start_date", "end_date", "description", "genre", "city"], dropna=False)
    .agg({"state": lambda x: ", ".join(sorted(set(x.dropna())))})
    .reset_index()
)
grouped = grouped.sort_values(by="start_date")
available_months = sorted(grouped["start_date"].dropna().apply(lambda d: (d.year, d.month)).unique())

if "month_index" not in st.session_state:
    st.session_state.month_index = 0

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("← Previous"):
        if st.session_state.month_index > 0:
            st.session_state.month_index -= 1
with col3:
    if st.button("Next →"):
        if st.session_state.month_index < len(available_months) - 1:
            st.session_state.month_index += 1

if available_months:
    selected_year, selected_month = available_months[st.session_state.month_index]

    st.markdown(
        f"<h2>📅 Festivals in {calendar.month_name[selected_month]} {selected_year}</h2>",
        unsafe_allow_html=True,
    )

    this_month = grouped[
        (grouped["start_date"].dt.year == selected_year) &
        (grouped["start_date"].dt.month == selected_month)
    ].reset_index(drop=True)

    cards_per_row = 3
    for i in range(0, len(this_month), cards_per_row):
        row_festivals = this_month.iloc[i : i + cards_per_row]
        cols = st.columns(cards_per_row)
        for col, (_, row) in zip(cols, row_festivals.iterrows()):
            with col:
                start = row['start_date'].date()
                end = row['end_date'].date() if pd.notnull(row['end_date']) else None
                date_str = f"{start}" if not end or start == end else f"{start} → {end}"
                st.markdown(
                    f"""
                    <div class="festival-card">
                        <h3>{row['festival_name']}</h3>
                        <p><strong>📍 City:</strong> {row['city']}</p>
                        <p><strong>📍 State(s):</strong> {row['state']}</p>
                        <p><strong>🎵 Genre:</strong> {row['genre']}</p>
                        <p><strong>📆 Date:</strong> {date_str}</p>
                        <details>
                            <summary>Details</summary>
                            <p>{row['description']}</p>
                        </details>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
else:
    st.info("No festival data available.")


