import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,BrowserConfig,CacheMode
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai import LLMConfig
import json
async def main():
    browser_config = BrowserConfig(headless=False)

    
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"
    run_config = CrawlerRunConfig(cache_mode = CacheMode.BYPASS,extraction_strategy=JsonCssExtractionStrategy(schema))

    async with AsyncWebCrawler(config = browser_config) as crawler:
        result = await crawler.arun(url = "raw://"+raw_html, config=run_config)

        data = json.loads(result.extracted_content)

        print(data)

asyncio.run(main())