import asyncio
from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig

async def multiple_page_crawl():
    browser_config = BrowserConfig(headless = True, java_script_enabled=True)
    url_lists = ["https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"]
    run_config = CrawlerRunConfig(cache_mode = CacheMode.BYPASS)

    async with AsyncWebCrawler(config = browser_config) as crawler:
        result = await crawler.arun_many(urls = url_lists, config = run_config)
        for res in result:
            print(res.markdown)

asyncio.run(multiple_page_crawl())