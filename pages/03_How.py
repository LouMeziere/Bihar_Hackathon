import streamlit as st
import pandas as pd

from utils.helpers import render_sidebar
import streamlit.components.v1 as components

# Sidebar filters
selected_states, selected_months = render_sidebar()

# Section title
st.markdown("""
<div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">HOW </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">the journey goes</span>
</div>
""", unsafe_allow_html=True)


# Inject custom CSS
st.markdown(
    """
    <style>

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
    st.markdown("<h1>What We Touch -- Made from Artisans</h1>", unsafe_allow_html=True)

    # Load and filter art data
    df_art = pd.read_csv("datasets/arts.csv", encoding='windows-1252')
    GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"
    df_art["image_url"] = df_art["image_url"].apply(lambda x: f"{GITHUB_BASE}/images/arts_out/{x}")

    # Load people benefited data and clean it
    df_benefit = pd.read_csv("datasets/person_benefited_handicraft.csv", encoding='windows-1252')
    df_benefit.columns = df_benefit.columns.str.strip().str.lower().str.replace(" ", "_")
    df_benefit.rename(columns={"state/uts": "state", "total_no._of_persons_benefitted": "benefited"}, inplace=True)

    # Merge datasets on 'state'
    arts_filtered = df_art.merge(df_benefit[["state", "benefited"]], on="state", how="left").sort_values(by="state").copy()

    # Filter by selected states
    if selected_states:
        arts_filtered = arts_filtered[arts_filtered["state"].isin(selected_states)]

    # Generate carousel items
    carousel_items = ""
    for _, row in arts_filtered.iterrows():
        item_html = f"""
        <div class="carousel-item" data-benefit="{row['benefited']}" data-state="{row['state']}">
            <img src="{row['image_url']}" alt="{row['name']}">
            <div class="carousel-title">{row['name']}</div>
            <div class="carousel-text">📍 {row['state']}</div>
        </div>
        """
        carousel_items += item_html

    carousel_html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: auto; position: relative;">

    <style>
        .buy-local-card {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(to right, #2f5454, #1e2f2f);
        padding: 24px 32px;
        border-radius: 12px;
        color: #ffffff;
        margin: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        .buy-local-left {{
        max-width: 55%;
        }}
        .buy-local-title {{
        font-size: 26px;
        font-weight: 700;
        color: #34f4a4;
        margin-bottom: 12px;
        }}
        .buy-local-text {{
        font-size: 16px;
        line-height: 1.5;
        color: #b1c1b7;
        }}
        .buy-local-right {{
        text-align: center;
        max-width: 40%;
        }}
        .buy-local-number {{
        font-size: 50px;
        font-weight: 900;
        color: #34f4a4;
        margin-bottom: 6px;
        }}
        .buy-local-label {{
        font-weight: 600;
        font-size: 18px;
        color: #ffffff;
        }}

        .carousel-wrapper {{
        overflow: hidden;
        width: 100%;
        position: relative;
        height: 420px;  /* bigger height to fit bigger image */
        margin-bottom: 20px;
        }}
        .carousel-track {{
        display: flex;
        transition: transform 0.5s ease-in-out;
        height: 100%;
        }}
        .carousel-item {{
        flex: 0 0 100%;
        box-sizing: border-box;
        padding: 20px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        }}
        .carousel-item img {{
        max-height: 550px;   /* bigger image */
        max-width: 105%;     /* wider image */
        width: auto;
        border-radius: 8px;
        margin-bottom: 12px;
        object-fit: contain;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        user-select: none;
        pointer-events: none;
        }}
        .carousel-title, .carousel-text {{
            position: absolute;
            left: 20px;
            color: #34f4a4;
            text-shadow: 0 0 6px rgba(0,0,0,0.7);
            z-index: 12;
            max-width: 70%;
            pointer-events: none;
        }}
        .carousel-title {{
        top: 20px;
        font-size: 28px;
        font-weight: 700;
        color: #34f4a4;
        margin-bottom: 8px;
        }}
        .carousel-text {{
        top: 60px;
        font-size: 18px;
        font-weight: 500;
        color: #b1c1b7;
        }}

        /* Hide default buttons container */
        .carousel-buttons {{
        display: none;
        }}

        /* Arrow buttons styles */
        .carousel-arrow {{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0,0,0,0.7);
        border-radius: 50%;
        width: 48px;
        height: 48px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: background-color 0.3s ease;
        user-select: none;
        z-index: 10;
        }}
        .carousel-arrow:hover {{
        background: rgba(0,0,0,0.9);
        }}
        .carousel-arrow svg {{
        fill: #34f4a4;
        width: 24px;
        height: 24px;
        }}

        .arrow-left {{
        left: 12px;
        }}
        .arrow-right {{
        right: 12px;
        }}
    </style>

    <div class="buy-local-card">
        <div class="buy-local-left">
        <div class="buy-local-title">Buy Local</div>
        <div class="buy-local-text">
            Purchasing local crafts across India supports thousands of artisans and their families.<br><br>
            Every purchase from a local artisan strengthens their community, preserves cultural <br>
            traditions, and fosters sustainable tourism. 🌿
        </div>
        </div>
        <div class="buy-local-right">
        <div class="buy-local-number" id="benefitNumber">{arts_filtered.iloc[0]['benefited']}</div>
        <div class="buy-local-label" id="benefitLabel">people benefited in <br>{arts_filtered.iloc[0]['state']}</div>
        </div>
    </div>

    <div class="carousel-wrapper">
        <div class="carousel-track" id="carouselTrack">
        {carousel_items}
        </div>

        <!-- Left arrow -->
        <div class="carousel-arrow arrow-left" onclick="prev()" role="button" aria-label="Previous">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
        </div>

        <!-- Right arrow -->
        <div class="carousel-arrow arrow-right" onclick="next()" role="button" aria-label="Next">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8.59 16.59 10 18l6-6-6-6-1.41 1.41L13.17 12z"/></svg>
        </div>
    </div>

    <script>
        const track = document.getElementById("carouselTrack");
        const items = document.querySelectorAll(".carousel-item");
        let currentIndex = 0;

        function updateStats(index) {{
        const benefit = items[index].dataset.benefit;
        const state = items[index].dataset.state;
        document.getElementById("benefitNumber").textContent = benefit;
        document.getElementById("benefitLabel").innerHTML = `people benefited in <br>${{state}}`;
        }}

        function next() {{
        if (currentIndex < items.length - 1) {{
            currentIndex++;
            track.style.transform = `translateX(-${{100 * currentIndex}}%)`;
            updateStats(currentIndex);
        }}
        }}

        function prev() {{
        if (currentIndex > 0) {{
            currentIndex--;
            track.style.transform = `translateX(-${{100 * currentIndex}}%)`;
            updateStats(currentIndex);
        }}
        }}
    </script>

    </div>
    """


    components.html(carousel_html, height=850)









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
