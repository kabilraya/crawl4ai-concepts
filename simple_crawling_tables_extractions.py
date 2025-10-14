import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig,CrawlerRunConfig

async def table_extraction_from_crawling():
    browser_config = BrowserConfig(headless = True, verbose = True)

    run_conf = CrawlerRunConfig(cache_mode = CacheMode.BYPASS, table_score_threshold = 7, word_count_threshold=True, exclude_external_images=True, excluded_tags = ["header","nav"],process_iframes=True)

    async with AsyncWebCrawler(config = browser_config) as crawler:
        results = await crawler.arun("https://www.w3schools.com/html/html_tables.asp", config = run_conf)

        if results.success and results.tables:
            for i, table in enumerate(results.tables):
                print(f"\n Table: {i+1}")
                print(f"Caption: {table.get('Caption','No Caption')}")
                print(f"Headers: {table['headers']}")
                print(f"Rows: {len(table['rows'])}")

                for j,row in enumerate(table["rows"]):
                    print(f"{j+1} {row}")

asyncio.run(table_extraction_from_crawling())

