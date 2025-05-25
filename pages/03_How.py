# -------------------------------
#           Imports
# -------------------------------


import json
import pydeck as pdk
import pandas as pd
import altair as alt
import streamlit as st
import streamlit.components.v1 as components
from utils.helpers import render_sidebar, load_table,  month_order, GITHUB_BASE




# -------------------------------
#          Intro Section
# -------------------------------

# Display options of states and months in side bar
selected_states, selected_months = render_sidebar()

# Title
st.markdown("""
<div style="text-align: left; margin-top: 40px; margin-bottom: 0px;">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">HOW </span>
  <span style="color: white; font-size: 58px; font-weight: 600;">the journey goes</span>
</div>
""", unsafe_allow_html=True)




# -------------------------------
#         Ashrams Section
# -------------------------------

# Sub-title
st.markdown("<h2 style='color: #ffffff; margin_bottom: 0px; padding-bottom: 0px; padding-top: 50px;'>A Pause with Purpose</h2>", unsafe_allow_html=True)

# Description
st.markdown("""
<div style='color:#93aca4; padding-top:20px;'>
    A visit to an Indian ashram is not just a retreat — it is a return to yourself. 
    In these sacred spaces, time slows, clarity sharpens, and the noise of modern life gives way to deep inner peace. 
    Whether you are seeking healing, growth, or stillness, an ashram offers a journey inward that every traveler deserves to experience.
</div>
""", unsafe_allow_html=True)

# Lessons
st.markdown("""
<div style='margin-top: 30px; padding: 20px; background-color: #041c1c; border-left: 4px solid #34f4a4; border-radius: 6px; max-width: 700px; text-align:center;'>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 16px; margin-bottom: 20px;'>
        <span>🧘 <i>"Observe yourself gently — in awareness, transformation begins."</i></span>
        <span style='color: #34f4a4; font-weight: bold;'>Lesson 01</span>
    </div>
    <div style='display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 16px;'>
        <span>🌿 <i>"Balance giving to others with giving back to yourself."</i></span>
        <span style='color: #34f4a4; font-weight: bold;'>Lesson 02</span>
    </div>
</div>
""", unsafe_allow_html=True)





# --- Load & clean data ---

df_ashrams = load_table("ashrams")

# Drop null values
df_ashrams.dropna(inplace=True)

# Filter by selected states
if selected_states:
    df_ashrams = df_ashrams[df_ashrams["state"].isin(selected_states)]


df_ashrams["image_url"] = df_ashrams["image_url"].apply(lambda x: f"{GITHUB_BASE}/images/ashrams/{x}")

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
for idx, row in df_ashrams.iterrows():
    
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
st.components.v1.html(carousel_html, height=540, scrolling=False)










st.markdown("</div></div>", unsafe_allow_html=True)














# -------------------------------
#         Train Section
# -------------------------------

# Sub-title
st.markdown('<h1 class="title" style="color:#ffffff;">Where the Journey Is the Destination</h1>', unsafe_allow_html=True)

# Description
st.markdown(
    """
    <p class="subtitle">
    India boasts the world’s <strong style="color:#1c4c54;">second largest</strong> railway system, moving millions of travelers every day.<br>
    Taking an overnight train is a classic way to experience the country—offering genuine encounters with locals and a window into India’s vast and varied landscape.<br>
    Discover the charm of long-distance journeys or enjoy picturesque trips on narrow-gauge railways, including <strong style="color:#1c4c54;">3 UNESCO-recognized mountain 
    routes:</strong>  Darjeeling, Nilgiri, and Kalka-Shimla.<br><br>
    </p>
    """,
    unsafe_allow_html=True,
)




# --- Load & clean data --

# Load tables into dataframes
df_emissions = load_table("co2_emissions_transports")


st.markdown(
    """
    <style>
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




# --- Plot --

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
    alt.Chart(df_emissions)
    .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
    .encode(
        y=alt.Y('mode:N', sort='-x', title=None,
                axis=alt.Axis(labelColor='rgba(255, 255, 255, 0.8)', domainColor='#93aca4', tickColor='#93aca4')),
        x=alt.X('transport_gm_tkm', title='CO₂ Emissions (gm/tkm)', 
                axis=alt.Axis(labelColor='rgba(255, 255, 255, 0.8)', domainColor='#93aca4', tickColor='#93aca4', gridColor='rgba(255, 255, 255, 0.3)')),
        color=alt.Color('mode:N', scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values())), legend=None),
        tooltip=['mode', 'category', alt.Tooltip('transport_gm_tkm', format='.0f')]
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
        padding-bottom: 30px;
    ">
        <strong style="color:#34f4a4;">Insight:</strong> Rail transport (both freight and passenger) produces <span style="color:#1c4c54;">significantly lower CO₂ emissions</span> compared to road freight, passenger cars, and airways.<br>
        Choosing trains supports sustainable travel and reduces environmental impact across India.
    </div>
    """,
    unsafe_allow_html=True
)
# Spacer for gap
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)



# -------------------------------
#      Train Routes Section
# -------------------------------


with open("images/railway/railways_lines.geojson") as f:
    lines_data = json.load(f)

with open("images/railway/railways_points.geojson") as f:
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























# -------------------------------
#         Arts Section
# -------------------------------


# Sub-title 
st.markdown("""
<h2 style="color:#ffffff; text-align:left; font-weight: 900; font-size: 44px; margin: 40px 0 20px 0;">Local Artistry</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color:#93aca4;">Come home with more than souvenirs — buy handcrafted gifts that support artisans and preserve tradition.</div>
""", unsafe_allow_html=True)


# --- Load & clean data ---

# Load tables into dataframes
df_art = load_table("arts")
df_benefit = load_table("person_benefited_handicraft")

# Append full path in the 'image_url' column 
df_art["image_url"] = df_art["image_url"].apply(lambda x: f"{GITHUB_BASE}/images/arts_out/{x}")

# Rename specific columns 
df_benefit.rename(columns={
    "state_uts": "state",
    "total_no_of_persons_benefitted": "benefited"
}, inplace=True)

# Merge datasets on 'state'
arts_filtered = df_art.merge(df_benefit[["state", "benefited"]], on="state", how="left").sort_values(by="state").copy()

# Filter by selected states
if selected_states:
    arts_filtered = arts_filtered[arts_filtered["state"].isin(selected_states)]

# Show if no data after filter
if arts_filtered.empty:
    st.markdown("")
    st.info("No local artistry for this selection.")
else:
    # Generate carousel items
    carousel_items = ""
    for _, row in arts_filtered.iterrows():
        item_html = f"""
        <div class="carousel-item" data-benefit="{row['benefited']}" data-state="{row['state']}">
            <img src="{row['image_url']}" alt="{row['name']}">
            <div class="carousel-info-box">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 30px 12px; border-radius: 0 0 12px 12px; height: 70px; ];">
                <div class="carousel-arrow arrow-left" onclick="prev()" role="button" aria-label="Previous">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
                </svg>
                </div>
                
                <div style="text-align: center;">
                <div class="carousel-title">{row['name']}</div>
                <div class="carousel-text">📍 {row['state']}</div>
                </div>

                <div class="carousel-arrow arrow-right" onclick="next()" role="button" aria-label="Next">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8.59 16.59 13.17 12 8.59 7.41 10 6l6 6-6 6z"/>
                </svg>
                </div>
            </div>
            </div>

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
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
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
        width: 600px;
        position: relative;
        height: auto;  /* bigger height to fit bigger image */
        margin: 0 auto 20px auto;
        align: center;
        }}
        .carousel-track {{
        display: flex;
        transition: transform 0.5s ease-in-out;
        height: 100%;
        }}
        .carousel-item {{
        flex: 0 0 100%;
        box-sizing: border-box;
        padding: 0px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        }}
        .carousel-item img {{
        height: 300px;
        width: 100%;
        object-fit: cover; /* Crops but maintains aspect ratio */
        border-radius: 8px 8px 0 0;
        margin-bottom: 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        user-select: none;
        pointer-events: none;
        }}

        .carousel-title, .carousel-text {{
            position: static;
            color: #34f4a4;
            text-shadow: 0 0 6px rgba(0,0,0,0.7);
            z-index: 12;
            max-width: 100%;
            pointer-events: auto;
            text-align: center;
        }}
        .carousel-info-box {{
        background-color: #1e2f2f;
        padding: 12px 16px;
        width: 100%;
        color: #ffffff;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin-top: 8px;
        border-radius: 0 0 8px 8px;
        
        }}
        .carousel-title {{
        font-size: 20px;
        font-weight: bold;
        color: #34f4a4;
        margin-bottom: 4px;
        position: static;
        }}
        .carousel-text {{
        font-size: 14px;
        color: #b1c1b7;
        position: static;
        text-align: center;
        }}

        /* Hide default buttons container */
        .carousel-buttons {{
        display: none;
        }}

        /* Arrow buttons styles */
        .carousel-arrow {{
        top: auto;
        transform: none;
        background: rgba(4, 28, 28, 0.7);
        border-radius: 12px;
        width: 48px;
        height: 48px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: background-color 0.3s ease;
        user-select: none;
        z-index: 10;
        position: static;
        padding: 0 5px;
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
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        }}
        .arrow-right {{
        right: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
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
        <div class="buy-local-number" id="benefitNumber">{int(arts_filtered.iloc[0]['benefited'])}</div>
        <div class="buy-local-label" id="benefitLabel">people benefited in <br>{arts_filtered.iloc[0]['state']}</div>
        </div>
    </div>

    <div class="carousel-wrapper">
        <div class="carousel-track" id="carouselTrack">
        {carousel_items}
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
















