# 🇮🇳 India's Cultural Explorer

**India's Cultural Explorer** is a visual guide and interactive tool for 
travelers interested in exploring the cultural, historical, and environmental 
richness of India. The platform helps users answer essential questions about 
their journey — **where to go**, **when to go**, and **how to travel 
responsibly.

Users can:
- Discover UNESCO heritage sites, sacred spaces, and festivals across India
- Get travel recommendations including the best seasons for ideal weather
- Explore Indian arts, handicrafts, and immersive experiences
- Understand the environmental impact of different transportation modes
- Learn how responsible tourism benefits communities and supports sustainability

---

## 📊 Datasets

All datasets used are publicly available or taken from official government and
tourism sources. Below is a detailed list with sources and notes:

- **UNESCO Sites per Country** (`Unesco_sites_per_country.csv`)  
  **Source**: [UNESCO World Heritage Centre](https://whc.unesco.org/en/list/stat/)  
  - Data up to date as of May 20, 2025.

- **Tourism Statistics**  
  **Source**: *2024 India Tourism Data Compendium*, Ministry of Tourism  
  - Website: [https://tourism.gov.in/](https://tourism.gov.in/)  
  - Used for state-wise tourism heatmap and visitor flow. Data reflects tourism activity from 2023–24.

- **Festivals in India**  
  **Source**: [Festivals From India](https://www.festivalsfromindia.org/)
  - Scraped data including upcoming festivals and descriptions. 

- **Ashrams in India**  
  **Source**: [Art of Living](https://www.artofliving.org/ashram/india)  
  - Includes ashram locations and descriptions.

- **Indian Railways Map Data**  
  **Source**: [Humanitarian Data Exchange (HDX)](https://data.humdata.org/)  
  - 2 GeoJSON format railway map data making up both lines and points.

- **Handicrafts & Arts of India**  
  - Arts and crafts descriptions:  
    [Incredible India - Exquisite Crafts](https://www.incredibleindia.gov.in/en/exquisite-crafts)  
  - Beneficiary data (`personBenefitedHandicraft.csv`):  
    [Data.gov.in](https://www.data.gov.in/resource/stateut-wise-number-persons-benefitted-under-handicrafts-sector-reply-starred-question-25)

- **Climate and Weather Data** (`weather_data`)  
  **Source**: [Climate-Data.org](https://en.climate-data.org/)  
  - Used to determine ideal travel months based on regional climate conditions. Temperatures are averages from 1999 - 2019

---

## ▶️ How to Run

To launch the application locally, run:

```bash
streamlit run Home.py
