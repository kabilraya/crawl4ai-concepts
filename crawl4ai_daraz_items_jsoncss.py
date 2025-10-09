import asyncio
from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig,JsonCssExtractionStrategy
import json

async def daraz_items_extraction():
    schema = {
        "name": "Daraz Items",
        # This base selector targets each product card on the page
        "baseSelector": "div[data-qa-locator='product-item']",
        "fields": [
            {
                "name": "product_name",
                # Selects the 'a' tag which contains the title
                "selector": "div.RfADt > a",
                "type": "attribute",
                "attribute": "title"
            },
            {
                "name": "price",
                # Selects the span containing the price
                "selector": "div:nth-child(2) > div:nth-child(3) > span",
                "type": "text"
            }
        ]
    }

    browser_config = BrowserConfig(headless = False)
    crawler_config = CrawlerRunConfig(extraction_strategy = JsonCssExtractionStrategy(schema),cache_mode = CacheMode.BYPASS)

    async with AsyncWebCrawler(config = browser_config) as crawler:
        result = await crawler.arun(url = "https://www.daraz.com.np/measuring-levelling/?from=suggest_normal&q=camera",config = crawler_config)
        data = json.loads(result.extracted_content)

        print(data)

asyncio.run(daraz_items_extraction())