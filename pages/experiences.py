import streamlit as st
import pandas as pd
import calendar
from utils.helpers import render_sidebar

# Sidebar filters
selected_states, selected_months = render_sidebar()



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
        background: rgba(0, 0, 0, 0.55);
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
        color: #F59C23;
        margin-bottom: 30px;
    }

    .experience-button {
        background-color: #F59C23;
        color: #fff;
        border: none;
        padding: 10px 22px;
        border-radius: 6px;
        font-size: 16px;
        font-weight: 600;
        margin-top: 20px;
        cursor: pointer;
    }

    .experience-button:hover {
        background-color: #dd8800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Section background with overlay
st.markdown("""
<div class="experience-section" style="background-image: url('https://images.unsplash.com/photo-1578926375605-9d3f5dcfac96');">
  <div class="experience-overlay">
    <div class="experience-title">A Date</div>
    <div class="experience-subtitle">When India comes alive with colors, lights, and rhythm.</div>
""", unsafe_allow_html=True)

# Expand to show festival details
if st.button("Explore Festivals", key="festivals_btn", use_container_width=True):
    st.session_state.show_festivals = not st.session_state.get("show_festivals", False)

if st.session_state.get("show_festivals", False):
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
            background: #262730;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 1.5rem;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
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
            color: #2c3e50;
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
        /* Details summary styling */
        details summary {
            cursor: pointer;
            font-weight: 600;
            color: #2980b9;
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
            color: #34495e;
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
<div class="experience-section" style="background-image: url('https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0');">
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
            background-color: #000;
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
            width: 350px;
            height: 400px;
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            box-shadow: 0 0 20px rgba(255,255,255,0.15);
        }
        .ashram-overlay {
            background: linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0.2));
            position: absolute;
            bottom: 0;
            padding: 20px;
            width: 100%;
            color: white;
        }
        .ashram-name {
            font-size: 22px;
            font-weight: bold;
            color: #F59C23;
        }
        .ashram-meta {
            font-size: 13px;
            opacity: 0.8;
            margin-top: 5px;
        }
        .ashram-desc {
            font-size: 14px;
            margin-top: 10px;
            line-height: 1.4;
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
    st.markdown("<h2 style='color:#F59C23; text-align:center;'>Sacred Spaces Across India</h2>", unsafe_allow_html=True)
    st.components.v1.html(carousel_html, height=600, scrolling=False)



st.markdown("</div></div>", unsafe_allow_html=True)
