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





# Load feedback data directly from Snowflake
try:
    # Replace 'YOUR_SCHEMA_NAME' with your actual Snowflake schema (e.g., 'discover_india.public')
    feedback_df = load_table("FEEDBACK_DATA", schema="PUBLIC")
except Exception as e:
    # If loading fails, display error message and create empty DataFrame with expected columns
    st.error(f"Failed to load feedback data: {e}")
    feedback_df = pd.DataFrame(columns=["name", "feedback", "rating"])

# Display the average rating and total number of reviews if data exists
if not feedback_df.empty:
    avg_rating = feedback_df["rating"].mean()  # Calculate average rating
    total_ratings = feedback_df["rating"].count()  # Count total number of ratings
    st.markdown(
        f"<h2 style='color:#ffffff; padding-top:50px;'>⭐ Current Rating: {avg_rating:.0f} / 5 ({total_ratings} reviews)</h2>",
        unsafe_allow_html=True
    )
else:
    # Message to show if no feedback data is available yet
    st.markdown(
        "<h2 style='color:#ffffff;padding-top:50px;'>⭐ No ratings yet. Be the first to give feedback!</h2>",
        unsafe_allow_html=True
    )

# Dictionary mapping rating values to descriptive text
rating_descriptions = {
    1: "Poor",
    2: "Fair",
    3: "Decent",
    4: "Good",
    5: "Excellent"
}

# Show rating options for user to select
st.markdown("**Rate us:**")
rating = st.radio(
    label="",  # Hide the label
    options=[5, 4, 3, 2, 1],  # Ratings from 5 (best) to 1 (worst)
    index=0,  # Default selection (5 stars)
    key="rating",
    label_visibility="collapsed",  # Collapse label to save space
    horizontal=True,  # Display radio buttons horizontally
)

# Display textual description for the selected rating
desc = rating_descriptions.get(rating, "")
st.markdown(f"<div class='rating-desc'>{desc}</div>", unsafe_allow_html=True)

# Feedback submission form
with st.form("feedback_form"):
    name = st.text_input("Your name (optional)")  # Optional name input
    feedback = st.text_area("Your feedback", placeholder="Tell us what you think...")  # Feedback textarea
    submit = st.form_submit_button("Submit")  # Submit button

    if submit:
        # When submitted, insert new feedback record directly into Snowflake
        upload_feedback_to_snowflake(name, feedback, rating)
        
        # Show success message to user
        st.success("Thank you for your feedback!")