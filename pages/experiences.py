import streamlit as st
import pandas as pd
import calendar
from utils.helpers import render_sidebar


selected_states, selected_months = render_sidebar()

st.subheader("Experiences of a life time")

df_festival = pd.read_csv("datasets/festivals.csv", encoding='windows-1252')
df_festival = df_festival.dropna(subset=['state'])

# Ensure datetime columns
df_festival["start date"] = pd.to_datetime(df_festival["start date"], errors="coerce")
df_festival["end date"] = pd.to_datetime(df_festival["end date"], errors="coerce")

# Apply filters
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
        filtered_festivals["start date"].dt.month.isin(selected_month_nums)
    ]

# Combine entries with the same festival but different states
grouped = (
    filtered_festivals
    .groupby(["festival", "start date", "end date", "description"], dropna=False)
    .agg({"state": lambda x: ", ".join(sorted(set(x.dropna())))})
    .reset_index()
)

# Sort by start date
grouped = grouped.sort_values(by="start date")









# Step 1: Get available (year, month) pairs
available_months = sorted(grouped["start date"].dropna().apply(lambda d: (d.year, d.month)).unique())

# Step 2: Initialize session state
if "month_index" not in st.session_state:
    st.session_state.month_index = 0

# Step 3: Add navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Previous"):
        if st.session_state.month_index > 0:
            st.session_state.month_index -= 1
with col3:
    if st.button("Next →"):
        if st.session_state.month_index < len(available_months) - 1:
            st.session_state.month_index += 1

# Step 4: Display festivals for current month only
if available_months:
    selected_year, selected_month = available_months[st.session_state.month_index]
    st.subheader(f"📅 Festivals in {calendar.month_name[selected_month]} {selected_year}")

    this_month = grouped[
        (grouped["start date"].dt.year == selected_year) &
        (grouped["start date"].dt.month == selected_month)
    ].reset_index(drop=True)

    cards_per_row = 3
    for i in range(0, len(this_month), cards_per_row):
        row_festivals = this_month.iloc[i : i + cards_per_row]
        cols = st.columns(cards_per_row)

        for col, (_, row) in zip(cols, row_festivals.iterrows()):
            with col:
                st.markdown(f"### {row['festival']}")
                start = row['start date'].date()
                end = row['end date'].date() if pd.notnull(row['end date']) else None
                date_str = f"{start}" if not end or start == end else f"{start} → {end}"
                st.markdown(f"**📍 State(s):** {row['state']}")
                st.markdown(f"**📆 Date:** {date_str}")

                with st.expander(f"Details"):
                    st.markdown(row['description'])
                st.markdown("---")
else:
    st.info("No festival data available.")


