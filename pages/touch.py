import streamlit as st
import pandas as pd
from streamlit_carousel import carousel
from utils.helpers import render_sidebar

selected_states, selected_months = render_sidebar()

st.markdown("<h1>What We Touch -- Made from Artisans</h1>", unsafe_allow_html=True)




# 🎨 Intro section
st.subheader("🎨 Traditional Art Forms")
st.markdown(
    """
    *Travel is more than just seeing new places — it's about connecting with the heart of a culture.*  
    Whenever possible, choose to buy handicrafts and souvenirs directly from **local artisans** or **non-profit cooperatives**.

    Your choices help sustain centuries-old traditions, empower communities, and breathe life into regional art forms.  
    Let's make every purchase count. 💫
    """
)




# 📦 Load and filter art data
df_art = pd.read_csv("datasets/arts.csv", encoding='windows-1252')
GITHUB_BASE = "https://raw.githubusercontent.com/LouMeziere/Bihar_Hackathon/main"
df_art["image_url"] = df_art["image_url"].apply(lambda x: f"{GITHUB_BASE}/images/arts_out/{x}")

arts_filtered = df_art.sort_values(by="state").copy()
if selected_states:
    arts_filtered = arts_filtered[arts_filtered["state"].isin(selected_states)]

# 🖼️ Carousel of art items
if arts_filtered.empty:
    st.info("No traditional art forms found for the selected state(s).")
else:
    items = []
    for _, row in arts_filtered.iterrows():
        items.append({
            "title": row['name'],
            "text": f"📍 {row['state']}",
            "img": row["image_url"],  # just URL here
        })

    carousel(items)





# 📊 Impact section
df_benefits = pd.read_csv("datasets/person_benefited_handicraft.csv")
df_benefits.columns = df_benefits.columns.str.strip()  # Clean column names

benefits_map = dict(zip(df_benefits["State/UTs"], df_benefits["Total no. of Persons Benefitted"]))

st.markdown("### 👥 Impact of Supporting Local Artisans")
st.markdown(
    """
    Purchasing local crafts across India supports thousands of artisans and their families.
    For example:
    """
)

if selected_states:
    total_beneficiaries = 0
    for state in selected_states:
        if state in benefits_map:
            st.markdown(f"• **{state}**: {benefits_map[state]:,} artisans and community members benefited.")
            total_beneficiaries += benefits_map[state]
    st.markdown(
        f"""
        When you support local crafts in these selected states,  
        you contribute to the livelihood of over **{total_beneficiaries:,}** people. 💚 
        
        <br><br>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "- **Andhra Pradesh**: 18,457 people benefited  \n"
        "- **Arunachal Pradesh**: 5,126 people benefited  \n"
        "- **A & N Islands**: 8,938 people benefited  \n"
    )
    st.markdown(
        """
        Every purchase from a local artisan strengthens their community,  
        preserves cultural traditions, and fosters sustainable tourism. 🌿

        <br><br>
        """,
        unsafe_allow_html=True
    )
