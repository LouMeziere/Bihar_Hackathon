import streamlit as st
import pandas as pd
from utils.helpers import render_sidebar
import streamlit.components.v1 as components

selected_states, selected_months = render_sidebar()

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
        <div class="carousel-info-box">
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 12px; border-radius: 0 0 12px 12px; height: 70px;">
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























st.markdown("""
<div class="experience-section" style="background-image: url('https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main/images/a_feeling.jpg');">
  <div class="experience-overlay">
    <div class="experience-title">A Pause with Purpose</div>
    <div class="experience-subtitle">Find calm and clarity — experience spiritual spaces that invite reflection, healing, and connection.</div>
""", unsafe_allow_html=True)


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
