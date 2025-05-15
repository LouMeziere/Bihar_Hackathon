import asyncio
import pandas as pd
import re
import json
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    JsonCssExtractionStrategy
)

# Define genres and construct URLs
genres = {'music', 'multi-arts', 'literature', 'theatre'}
url = 'https://www.festivalsfromindia.com/genres/music/'

# Define the schema for data extraction
schema = {
    "name": "Festival Data",
    "baseSelector": "#loadmorepost",
    "fields": [
        {"name": "image", "selector": "article.festival img.wp-post-image", "type": "img"},
        {"name": "festival_name", "selector": "article.festival h4", "type": "text"},
        {"name": "genre", "selector": "article.festival span.cf-grids-box-cat-genre", "type": "text"},
        {"name": "city", "selector": "article.festival div.cf-grids-box-footer-first span.cf-grids-box-footer-location:nth-of-type(1)", "type": "text"},
        {"name": "state", "selector": "article.festival div.cf-grids-box-footer-first span.cf-grids-box-footer-location:nth-of-type(2)", "type": "text"},
        {"name": "start_date", "selector": "article.festival div.cf-grids-box-footer-last span.cf-grids-box-footer-date:nth-of-type(1)", "type": "text"},
        {"name": "end_date", "selector": "article.festival div.cf-grids-box-footer-last span.cf-grids-box-footer-date:nth-of-type(2)", "type": "text"},
    ]
}
js_commands = [
    "window.scrollTo(0, document.body.scrollHeight);",
    "await new Promise(resolve => setTimeout(resolve, 3000));"  # wait 3s after scroll
]

# Cleaning function for city and state
def clean_location(text):
    return re.sub(r'[^\w\s]', '', text).strip()

# Cleaning function for date (e.g., "to 29 Jun 2025" -> "29 Jun 2025")
def clean_date(text):
    return re.sub(r'\bto\b', '', text, flags=re.IGNORECASE).strip()

# Main async function
async def main():
    print("Collecting data...")
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                js_code=js_commands,
                wait_for="js:() => document.querySelectorAll('article.festival img').length > 10",
                markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter()),
                extraction_strategy=JsonCssExtractionStrategy(schema)
            )
        )

    all_data = []

    # Print the extracted content
    for result in results:
        if result.success and result.extracted_content:
            data = json.loads(result.extracted_content)
            all_data.extend(data)  # Add the extracted items into the list
        else:
            print(f"Failed to extract: {result.url}")

    print(all_data)

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())

