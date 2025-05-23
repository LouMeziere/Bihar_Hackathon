import pandas as pd
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
import re


df = pd.DataFrame()

urls = [
    'https://en.climate-data.org/asia/india/maharashtra/amravati-993326/',
    'https://en.climate-data.org/asia/india/arunachal-pradesh/itanagar-24706/',
    'https://en.climate-data.org/asia/india/assam/dispur-47482/',
    'https://en.climate-data.org/asia/india/bihar/patna-4748/',
    'https://en.climate-data.org/asia/india/chhattisgarh/raipur-5085/',
    'https://en.climate-data.org/asia/india/goa/panaji-6394/',
    'https://en.climate-data.org/asia/india/gujarat/gandhinagar-5583/',
    'https://en.climate-data.org/asia/india/chandigarh/chandigarh-4075/',
    'https://en.climate-data.org/asia/india/himachal-pradesh/shimla-3891/',
    'https://en.climate-data.org/asia/india/jharkhand/ranchi-968991/',
    'https://en.climate-data.org/asia/india/karnataka/bengaluru-4562/',
    'https://en.climate-data.org/asia/india/kerala/thiruvananthapuram-2783/',
    'https://en.climate-data.org/asia/india/madhya-pradesh/bhopal-2833/',
    'https://en.climate-data.org/asia/india/maharashtra/mumbai-29/',
    'https://en.climate-data.org/asia/india/meghalaya/shillong-24618/',
    'https://en.climate-data.org/asia/india/mizoram/aizawl-24529/',
    'https://en.climate-data.org/asia/india/odisha/bhubaneswar-5756/',
    'https://en.climate-data.org/asia/india/chandigarh/chandigarh-4075/',
    'https://en.climate-data.org/asia/india/rajasthan/jaipur-3888/',
    'https://en.climate-data.org/asia/india/sikkim/gangtok-33807/',
    'https://en.climate-data.org/asia/india/tamil-nadu/chennai-1003222/',
    'https://en.climate-data.org/asia/india/hyderabad/hyderabad-2801/',
    'https://en.climate-data.org/asia/india/tripura/agartala-24533/',
    'https://en.climate-data.org/asia/india/uttar-pradesh/lucknow-2850/',
    'https://en.climate-data.org/asia/india/uttarakhand/dehradun-3679/',
    'https://en.climate-data.org/asia/india/west-bengal/kolkata-2826/'
]

city_to_state = {
    'Amravati': 'Maharashtra',
    'Itanagar': 'Arunachal Pradesh',
    'Dispur': 'Assam',
    'Patna': 'Bihar',
    'Raipur': 'Chhattisgarh',
    'Panaji': 'Goa',
    'Gandhinagar': 'Gujarat',
    'Chandigarh': 'Chandigarh',
    'Shimla': 'Himachal Pradesh',
    'Ranchi': 'Jharkhand',
    'Bengaluru': 'Karnataka',
    'Thiruvananthapuram': 'Kerala',
    'Bhopal': 'Madhya Pradesh',
    'Mumbai': 'Maharashtra',
    'Shillong': 'Meghalaya',
    'Aizawl': 'Mizoram',
    'Bhubaneswar': 'Odisha',
    'Jaipur': 'Rajasthan',
    'Gangtok': 'Sikkim',
    'Chennai': 'Tamil Nadu',
    'Hyderabad': 'Telangana',
    'Agartala': 'Tripura',
    'Lucknow': 'Uttar Pradesh',
    'Dehradun': 'Uttarakhand',
    'Kolkata': 'West Bengal'
}


def extract_first_number(value):
    if not isinstance(value, str):
        return value
    match = re.match(r"([-+]?\d+\.?\d*)", value)
    if match:
        return float(match.group(1))
    return None

def clean_humidity(humidity_str):
    if not isinstance(humidity_str, str):
        return humidity_str
    clean_str = humidity_str.replace('%', '').strip()
    try:
        return float(clean_str)
    except ValueError:
        return None

async def main():
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=CrawlerRunConfig(
                css_selector='section[itemscope]:not([class])'
            )
        )

    all_dfs = []
    for result in results:
        markdown_text = result.markdown or ""
        city_match = re.search(r'Weather by Month ([A-Z][\w\.\'-]*(?: [A-Z][\w\.\'-]*)*)', markdown_text)
        city = city_match.group(1) if city_match else "Unknown City"
        
        # Get state from dictionary; fallback to 'Unknown State'
        state = city_to_state.get(city, "Unknown State")

        if not result.tables:
            print(f"No tables found for city: {city}")
            continue

        weather_table = result.tables[0]
        headers = weather_table["headers"]
        if headers[0] == '' or headers[0] is None:
            headers[0] = "month"

        df = pd.DataFrame(weather_table["rows"], columns=headers)
        df["city"] = city
        df["state"] = state   # Add state column here

        # Clean temperature columns
        for col in ['Avg. Temperature °C (°F)', 'Min. Temperature °C (°F)', 'Max. Temperature °C (°F)']:
            if col in df.columns:
                df[col] = df[col].apply(extract_first_number)

        # Rename temperature columns
        df = df.rename(columns={
            'Avg. Temperature °C (°F)': 'Avg. Temperature (°C)',
            'Min. Temperature °C (°F)': 'Min Temperature (°C)',
            'Max. Temperature °C (°F)': 'Max Temperature (°C)'
        })

        # Clean rainfall column and rename
        rainfall_col = 'Precipitation / Rainfall mm (in)'
        if rainfall_col in df.columns:
            df[rainfall_col] = df[rainfall_col].apply(extract_first_number)
            df = df.rename(columns={rainfall_col: 'Rainfall (mm)'})

        # Clean humidity column (remove %)
        humidity_col = 'Humidity (%)'
        if humidity_col in df.columns:
            df[humidity_col] = df[humidity_col].apply(clean_humidity)

        # Reorder columns: city, state, month, rest
        cols = df.columns.tolist()
        for col in ['city', 'state', 'month']:
            if col in cols:
                cols.remove(col)
        df = df[['city', 'state', 'month'] + cols]

        all_dfs.append(df)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)

        pd.set_option('display.max_columns', None)
        print(final_df)

        # Save the final dataframe to CSV (overwrite each run)
        file_path = "datasets/weather_data.csv"
        final_df.to_csv(file_path, index=False)
        print(f"Saved data to {file_path}")

asyncio.run(main())