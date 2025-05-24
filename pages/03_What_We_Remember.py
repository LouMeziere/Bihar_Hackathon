import streamlit as st
import pandas as pd
import calendar
from utils.helpers import render_sidebar

# Sidebar filters
selected_states, selected_months = render_sidebar()

# Inject custom CSS
st.markdown(
    """
    <style>
    h1 {
        font-weight: 700;
        margin-bottom: 0.3rem;
        font-size: 2.5rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .experience-section {
        position: relative;
        margin: 40px 0;
        padding: 60px 40px;
        border-radius: 16px;
        color: white;
        text-align: center;
        background-size: cover;
        background-position: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    .experience-overlay {
        background: rgba(4, 28, 28, 0.75);
        padding: 60px 20px;
        border-radius: 16px;
    }

    .experience-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .experience-subtitle {
        font-size: 22px;
        color: #34f4a4;
        margin-bottom: 30px;
    }

    .experience-button {
        background-color: #041c1c;
        color: #fff;
        border: 2px solid #1c4c54 ;
        padding: 10px 22px;
        border-radius: 8px;
        font-size: 16px;
       
        cursor: pointer;
        width: 100%;
    }

    .experience-button:hover {
        color: #34f4a4;
        border: 1px solid #34f4a4;
    }

    .button-container {
        padding: 0 40px;
        margin-top: -20px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page title
st.markdown("<h1>What We Remember</h1>", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="experience-section" style="background-image: url('https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main/images/a_date.jpg');">
  <div class="experience-overlay">
    <div class="experience-title">A Date</div>
    <div class="experience-subtitle">When India comes alive with colors, lights, and rhythm.</div>
  </div>
</div>
""", unsafe_allow_html=True)



# Handle query param using updated API
if st.button("Explore Festivals", key="festivals_btn", use_container_width=True):
    st.session_state.show_festivals = not st.session_state.get("show_festivals", False)

if st.session_state.get("show_festivals"):
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



st.markdown("</div></div>", unsafe_allow_html=True)



st.markdown("""
<div class="experience-section" style="background-image: url('https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main/images/a_feeling.jpg');">
  <div class="experience-overlay">
    <div class="experience-title">A Feeling</div>
    <div class="experience-subtitle">A moment of stillness, a breath in the sacred hush.</div>
""", unsafe_allow_html=True)

if st.button("Explore Ashrams", key="ashrams_btn", use_container_width=True):
    st.session_state.show_ashrams = not st.session_state.get("show_ashrams", False)

if st.session_state.get("show_ashrams", False):

    # Load ashram data
    df = pd.read_csv("datasets/ashrams.csv", encoding='windows-1252')
    df.dropna(inplace=True)

    GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main/images/ashrams"
    df["image_url"] = df["image_url"].apply(lambda x: f"{GITHUB_BASE}/{x}")

    # Build carousel HTML with SwiperJS
    carousel_html = """
    <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
    />
    <style>
        body {
            color: white;
        }
        .swiper {
            width: 100%;
            padding-top: 50px;
            padding-bottom: 50px;
        }
        .swiper-slide {
            background-position: center;
            background-size: cover;
            width: 320px;
            height: 400px;
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            box-shadow: none;
        }
        .ashram-overlay {
            background: linear-gradient(to top, rgba(4, 28, 28, 0.7), rgba(28, 76, 84, 0.7));
            position: absolute;
            bottom: 0;
            padding: 20px;
            width: 100%;
        }
        .ashram-name {
            font-size: 22px;
            font-weight: bold;
            color: #34f4a4 !important;
            text-shadow: none;
            opacity: 1 ;
            
        }
        .ashram-meta {
            font-size: 13px;
            opacity: 1;
            margin-top: 5px;
        }
        .ashram-desc {
            font-size: 14px;
            margin-top: 10px;
            line-height: 1.4;
        }
        .swiper-button-next, .swiper-button-prev {
            color: #34f4a4; 
        }
        /* Change inactive pagination bullets */
        .swiper-pagination-bullet {
        background: #1c4c54 !important;
        opacity: 0.6;
        }

        /* Change active pagination bullet */
        .swiper-pagination-bullet-active {
        background: #34f4a4 !important;
        opacity: 1;
        }
       
    </style>

    <div class="swiper mySwiper">
    <div class="swiper-wrapper">
    """

    # Add each ashram card as a swiper slide
    for idx, row in df.iterrows():
        
        card_html = f"""
        <div class="swiper-slide" style="background-image: url('{row["image_url"]}');">
            <div class="ashram-overlay">
                <div class="ashram-name">{row['name']}, {row['state']}</div>
                <div class="ashram-meta">{row['phone']} | {row['email']}</div>
                <div class="ashram-desc">{row['description']}</div>
            </div>
        </div>
        """
        carousel_html += card_html

    carousel_html += """
    </div>
    <div class="swiper-pagination"></div>
    <div class="swiper-button-next"></div>
    <div class="swiper-button-prev"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
    const swiper = new Swiper(".mySwiper", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        pagination: {
        el: ".swiper-pagination",
        clickable: true,
        },
        navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
        },
        breakpoints: {
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
        },
    });
    </script>
    """

    # Show it in Streamlit
    st.markdown("<h2 style='text-align:center; margin_bottom: 0px; padding-bottom: 0px; padding-top: 70px;'>Sacred Spaces Across India</h2>", unsafe_allow_html=True)
    st.components.v1.html(carousel_html, height=600, scrolling=False)



st.markdown("</div></div>", unsafe_allow_html=True)











# Initialize session state if not already set
if "show_railways" not in st.session_state:
    st.session_state.show_railways = False

# A Journey Section
st.markdown("""
<div class="experience-section" style="background-image: url('https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main/images/a_journey.jpg');">
  <div class="experience-overlay">
    <div class="experience-title">A Journey</div>
    <div class="experience-subtitle">Tracing India’s heartbeat through the world’s second largest rail network.</div>
""", unsafe_allow_html=True)

if st.button("Explore Railways", key="rail_btn", use_container_width=True):
    st.session_state.show_railways = not st.session_state.show_railways

if st.session_state.show_railways:

    import streamlit as st
    import pandas as pd
    import altair as alt

    # Load CSV
    df = pd.read_csv('datasets/co2_emissions_transports.csv')

    # Clean column names
    df.columns = df.columns.str.strip()

    
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #101414;
            color: #93aca4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .title {
            color: #34f4a4;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 0.25rem;
        }
        .subtitle {
            margin-top: 0;
            color: #93aca4;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<h1 class="title">India\'s Railway & Transport CO₂ Emissions Overview</h1>', unsafe_allow_html=True)

    st.markdown(
        """
        <p class="subtitle">
        India’s extensive railway network is the world’s <strong>second largest</strong>, carrying millions of passengers daily.<br>
        It blends modern upgrades and luxury carriages with iconic historic routes like the UNESCO-listed mountain railways of Darjeeling, Nilgiri, and Kalka-Shimla.<br><br>
        Traveling by train is not only one of the most authentic ways to experience India’s diverse landscapes and culture but also a <strong>greener alternative</strong> to flying, producing far less carbon emissions.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Define color mapping matching your palette
    color_map = {
        'Rail': '#34f4a4',          # Light green
        'Road': '#1c4c54 ',          # Grey
        'Shipping': '#282434',          # Light green
        'Passenger Cars': '#041c1c',# Dark green
        'Airways': '#1e2f2f'        # Flashy green
    }

    # Build bar chart
    bar_chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            y=alt.Y('Mode:N', sort='-x', title=None,
                    axis=alt.Axis(labelColor='#93aca4', domainColor='#93aca4', tickColor='#93aca4')),
            x=alt.X('Transport (gm/tkm):Q', title='CO₂ Emissions (gm/tkm)', 
                    axis=alt.Axis(labelColor='#93aca4', domainColor='#93aca4', tickColor='#93aca4')),
            color=alt.Color('Mode:N', scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values())), legend=None),
            tooltip=['Mode', 'Category', alt.Tooltip('Transport (gm/tkm):Q', format='.0f')]
        )
        .properties(height=300, width=700)
        .configure_view(strokeWidth=0)
    )

    st.altair_chart(bar_chart, use_container_width=True)

    # Insight box styled with your dark green background and flashy green text
    st.markdown(
        """
        <div style="
            background-color:#041c1c;
            border-left: 6px solid #34f4a4;
            padding: 16px;
            border-radius: 6px;
            margin-top: 20px;
            color: #93aca4;
            font-size: 16px;
            font-weight: 600;
        ">
            <strong style="color:#34f4a4;">Insight:</strong> Rail transport (both freight and passenger) produces <span style="color:#1c4c54;">significantly lower CO₂ emissions</span> compared to road freight, passenger cars, and airways.<br>
            Choosing trains supports sustainable travel and reduces environmental impact across India.
        </div>
        """,
        unsafe_allow_html=True
    )






    import json
    import pydeck as pdk

    with open("datasets/railway/railways_lines.geojson") as f:
        lines_data = json.load(f)

    with open("datasets/railway/railways_points.geojson") as f:
        points_data = json.load(f)

    rail_layer = pdk.Layer(
        "GeoJsonLayer",
        lines_data,
        get_line_color=[255, 0, 0],
        get_line_width=2,
        pickable=True
    )

    points_layer = pdk.Layer(
        "GeoJsonLayer",
        points_data,
        get_fill_color=[52, 244, 164, 160],  # changed to green
        get_radius=1000,
        point_radius_min_pixels=2,
        point_radius_max_pixels=10,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=22.9734,
        longitude=78.6569,
        zoom=4,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(
        layers=[rail_layer, points_layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"}
    ))


st.markdown("</div></div>", unsafe_allow_html=True)
