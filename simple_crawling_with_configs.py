import asyncio
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig,BrowserConfig,CacheMode

async def simple_crawling_with_configs():
    browser_config = BrowserConfig(headless = True, verbose = True)

    run_conf = CrawlerRunConfig(cache_mode = CacheMode.BYPASS, word_count_threshold = 10, exclude_external_links = True, process_iframes = True, remove_overlay_elements = True)

    async with AsyncWebCrawler(config = browser_config) as crawler:
        results  = await crawler.arun(url = "https://www.daraz.com.np/#?", config = run_conf)
        

        for result in results:
                if result.success:
                    print(result.markdown[:500])
                
                    for image in result.media["images"]:
                        print(image["src"])
                
                    for link in result.links["internal"]:
                        print(link["href"])

asyncio.run(simple_crawling_with_configs())