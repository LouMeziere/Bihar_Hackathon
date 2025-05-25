# 🇮🇳 Discover India

**Discover India** is a visual guide and interactive tool for travelers interested in exploring the cultural, historical, and environmental richness of India. The platform helps users answer essential questions about their journey — **where to go**, **when to go**, and **how to travel responsibly**.

Users can:
- Discover UNESCO heritage sites, sacred spaces, and festivals across India
- Get travel recommendations including the best seasons for ideal weather
- Explore Indian arts, handicrafts, and immersive experiences
- Understand the environmental impact of different transportation modes
- Learn how responsible tourism benefits communities and supports sustainability

---

## 📊 Datasets

All datasets used are publicly available or taken from official government and tourism sources. Below is a detailed list with sources and notes:

- **UNESCO Sites per Country** (`Unesco_sites_per_country.csv`)  
  **Source**: [UNESCO World Heritage Centre](https://whc.unesco.org/en/list/stat/)  
  - Data up to date as of May 20, 2025.

- **Tourism Statistics**  
  **Source**: *2024 India Tourism Data Compendium*, Ministry of Tourism  
  - Website: [https://tourism.gov.in/](https://tourism.gov.in/)  
  - Used for state-wise tourism heatmap and visitor flow. Data reflects tourism activity from 2023–24.

- **Festivals in India**  
  - Festival names and descriptions:  
    [Ministry of Culture](https://www.indiaculture.gov.in/festivals-religious)  
    [Incredible India](https://www.incredibleindia.gov.in/en)  
  - Supplementary data scraped from:  
    [Festivals From India](https://www.festivalsfromindia.org/)

- **Ashrams in India**  
  **Source**: [Art of Living](https://www.artofliving.org/ashram/india)  
  - Includes ashram locations and descriptions.

- **Indian Railways Map Data**  
  **Source**: [Humanitarian Data Exchange (HDX)](https://data.humdata.org/)  
  - GeoJSON format railway map data.

- **Handicrafts & Arts of India**  
  - Arts and crafts descriptions:  
    [Incredible India - Exquisite Crafts](https://www.incredibleindia.gov.in/en/exquisite-crafts)  
  - Beneficiary data (`personBenefitedHandicraft.csv`):  
    [Data.gov.in](https://www.data.gov.in/resource/stateut-wise-number-persons-benefitted-under-handicrafts-sector-reply-starred-question-25)

- **Climate and Weather Data** (`weather_data`)  
  **Source**: [Climate-Data.org](https://en.climate-data.org/)  
  - Used to determine ideal travel months based on regional climate conditions.

---

## ▶️ How to Run

To launch the application locally, run:

```bash
streamlit run Home.py

# Datasets
- Unesco_sites_per_country.csv : data is from UNESCO (https://whc.unesco.org/en/list/stat/) and is up to date as of May 20, 2025.
- Tourism data: from report '2024 India Tourism Data Compendium' by Ministry of Tourism (published on https://tourism.gov.in/). tourism on map  is 2023-24 shown
- festivals names found in (https://www.indiaculture.gov.in/festivals-religious). festival information found in Incredible India (https://www.incredibleindia.gov.in/en)
- festivals scraped from 'Festivals from India'
- ashrams from Art of Living https://www.artofliving.org/ashram/india
ashram lessons https://www.manifestationscapital.com/news-1/seven-lessons-from-the-ashram
- indian railway data from Humanitarian Data Exchange (HDX) 
- arts from Incredible India (https://www.incredibleindia.gov.in/en/exquisite-crafts)
- personBenefitedHandicraft.csv : 2019 data from gov (https://www.data.gov.in/resource/stateut-wise-number-persons-benefitted-under-handicrafts-sector-reply-starred-question-25)
- weather_data: all from Climate Data (https://en.climate-data.org/)



If need be
When running scrape_weather.py, the latest version of CRAWL4AI can be unstable. if you decide to keep using the latest version (v0.6.0), simply rerun the script until no error occur in terminal when scraping each link. 