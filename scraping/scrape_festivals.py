import re
import html
import asyncio
import pandas as pd
import re
import json
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    JsonCssExtractionStrategy, 
    CacheMode
)

# Genres to scrape
genres = ['music', 'multi-arts', 'literature', 'theatre']
base_url = "https://www.festivalsfromindia.com/genres/{}/page/{}/?orderby=title"

# Define schema
schema = {
    "name": "Festival Data",
    "baseSelector": "article.festival",
    "fields": [
        {"name": "image", "selector": "article.festival img.wp-post-image", "type": "img"},
        {"name": "festival_name", "selector": "article.festival h4", "type": "text"},
        {"name": "genre", "selector": "article.festival span.cf-grids-box-cat-genre", "type": "text"},
        {"name": "city", "selector": "article.festival div.cf-grids-box-footer-first span.cf-grids-box-footer-location:nth-of-type(1)", "type": "text"},
        {"name": "state", "selector": "article.festival div.cf-grids-box-footer-first span.cf-grids-box-footer-location:nth-of-type(2)", "type": "text"},
        {"name": "start_date", "selector": "article.festival div.cf-grids-box-footer-last span.cf-grids-box-footer-date:nth-of-type(1)", "type": "text"},
        {"name": "end_date", "selector": "article.festival div.cf-grids-box-footer-last span.cf-grids-box-footer-date:nth-of-type(2)", "type": "text"},
        {"name": "detail_url", "selector": "a.cf-grids-box", "type": "attribute","attribute": "href"}
    ]
}

detail_schema = {
    "name": "Festival Detail",
    "baseSelector": "div.fi-content",
    "fields": [
        {"name": "description", "selector": "p:nth-of-type(1)", "type": "text"}
    ]
}


async def main():
    print("Collecting data...")
    all_data = []

    ### FIRST crawl to get all information of each event
    async with AsyncWebCrawler() as crawler:
        for genre in genres:
            page = 1
            total_count = 0
            while True:
                current_url = base_url.format(genre, page)
                print(f"Scraping: {current_url}")
                
                results = await crawler.arun(
                    url=current_url,
                    config=CrawlerRunConfig(
                        wait_for="js:() => document.querySelectorAll('article.festival img').length > 0",
                        page_timeout=20000,  # 20 seconds limit
                        markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter()),
                        extraction_strategy=JsonCssExtractionStrategy(schema)
                    )
                )

                page_data = []
                for result in results:
                    if result.success and result.extracted_content:
                        data = json.loads(result.extracted_content)
                        if isinstance(data, list):
                            page_data.extend(data)
                        else:
                            page_data.append(data)
                    else:
                        print(f"Failed to extract: {result.url}")

                if not page_data:
                    print(f"No more data on page {page} for genre {genre}")
                    break

                total_count += len(page_data)
                print(f"Retrieved {len(page_data)} festivals from {current_url} (Total so far: {total_count})")

                all_data.extend(page_data)
                page += 1

    # Clean up data
    df = pd.DataFrame(all_data)
    df['city'] = df['city'].apply(lambda x: re.sub(r'[^\w\s]', '', x).strip() if isinstance(x, str) else x)
    df['state'] = df['state'].apply(lambda x: re.sub(r'[^\w\s]', '', x).strip() if isinstance(x, str) else x)
    df['start_date'] = df['start_date'].apply(lambda x: re.sub(r'\bto\b', '', x).strip() if isinstance(x, str) else x)
    df['end_date'] = df['end_date'].apply(lambda x: re.sub(r'\bto\b', '', x).strip() if isinstance(x, str) else x)

    # Drop duplicate rows
    df = df.drop_duplicates()



    urls = df["detail_url"].tolist()
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(detail_schema)
            )
        )

        url_to_description = {}
        for result in results:
            if result.success and result.extracted_content:
                try:
                    data = json.loads(result.extracted_content)[0]
                    description = data.get("description", "").strip()
                    # Decode HTML entities if any
                    description = html.unescape(description)
                    # Remove straight and curly quotes
                    description = re.sub(r'[\'"“”‘’]', '', description)
                    url_to_description[result.url] = description
                    print(repr(description))  # Check output
                except Exception as e:
                    print(f"Error processing result from {result.url}: {e}")

        # Assign description based on the URL mapping
        df["description"] = df["detail_url"].map(url_to_description)

        # Drop the URL column
        df.drop("detail_url", axis=1, inplace=True)

        # Clean curly and straight quotes from descriptions
        def clean_description(text):
            if isinstance(text, str):
                return (text.strip()
                            .replace('“', '')
                            .replace('”', '')
                            .replace('‘', '')
                            .replace('’', '')
                            .replace('"', '')
                            .replace("'", ''))
            return text

        df["description"] = df["description"].apply(clean_description)





    # Save to CSV
    df.to_csv("festivals_data.csv", index=False)
    print("Saved all data to festivals_data.csv")

if __name__ == "__main__":
    asyncio.run(main())
