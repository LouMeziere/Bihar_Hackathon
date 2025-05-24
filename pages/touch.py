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



























