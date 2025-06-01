import streamlit as st
import pandas as pd
import os
from utils.helpers import inject_global_css, load_table, GITHUB_BASE
from table_creation_snowflake.add_new_ratings import upload_feedback_to_snowflake

inject_global_css()

# Title
st.markdown("""
<div style="text-align: left; margin: 40px auto; max-width:850px">
  <span style="color: #34f4a4; font-size: 65px; font-weight: 900;">WHERE </span>
  <span style="color: white; font-size: 54px; font-weight: 600;">the journey ends</span>
</div>
<p>
India’s cultural journey is not just about where you go — it is about how and when you explore. By choosing under-discovered states, traveling during culturally vibrant yet less crowded months, and embracing low-impact transport like trains, you open the door to more authentic encounters. Take moments to pause in places of peace — like ashrams — where the journey turns inward and transforms the traveler.
This guide empowers you to travel not only to India but with India — supporting communities, preserving heritage, and discovering the soul of a country through every step you take.
</p>
""", unsafe_allow_html=True)









st.markdown("""
    <style>

    /* Optional enhancement for focused inputs (keeps theme color) */
    *:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px #34f4a4 !important;
    }

    /* Custom input aesthetics */
    input[type="text"],
    textarea {
        border: 1px solid #282434;
        background-color: #041c1c;
        color: #ffffff;
        border-radius: 6px;
        padding: 10px;
    }

    textarea::placeholder {
        color: #93aca4;
    }

    /* Star rating description */
    .rating-desc {
        margin-top: 5px;
        font-size: 1.1rem;
        font-weight: bold;
        color: #34f4a4;
    }
    .container h2 {
    color: #ffffff !important;
    }

    </style>
""", unsafe_allow_html=True)


FEEDBACK_FILE = f"{GITHUB_BASE}/datasets/feedback_data.csv"

# Load existing feedback if file exists; else create empty DataFrame (do NOT create file here)
if os.path.exists(FEEDBACK_FILE):
    feedback_df = load_table('feedback_data')
else:
    feedback_df = pd.DataFrame(columns=["name", "feedback", "rating"])

if not feedback_df.empty:
    avg_rating = feedback_df["rating"].mean()
    total_ratings = feedback_df["rating"].count()
    st.markdown(f"<h2 style='color:#ffffff; padding-top:50px;'>⭐ Current Rating:  {avg_rating:.0f} / 5 ({total_ratings} reviews)</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='color:#ffffff;padding-top:50px;'>⭐ No ratings yet. Be the first to give feedback!</h2>", unsafe_allow_html=True)

rating_descriptions = {
    1: "Poor",
    2: "Fair",
    3: "Decent",
    4: "Good",
    5: "Excellent"
}

st.markdown("**Rate us:**")

rating = st.radio(
    label="",
    options=[5, 4, 3, 2, 1],
    index=0,
    key="rating",
    label_visibility="collapsed",
    horizontal=True,
)

desc = rating_descriptions.get(rating, "")
st.markdown(f"<div class='rating-desc'>{desc}</div>", unsafe_allow_html=True)

with st.form("feedback_form"):
    name = st.text_input("Your name (optional)")
    feedback = st.text_area("Your feedback", placeholder="Tell us what you think...")
    submit = st.form_submit_button("Submit")

    if submit:
        new_feedback = pd.DataFrame([{
            "name": name,
            "feedback": feedback,
            "rating": rating
        }])
        
        if not os.path.exists(FEEDBACK_FILE):
            # First submission: create file with header
            new_feedback.to_csv(FEEDBACK_FILE, index=False)
        else:
            # Append without header
            new_feedback.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)
        
        # Now push to Snowflake
        upload_feedback_to_snowflake()
        
        st.success("Thank you for your feedback!")