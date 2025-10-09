import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    #create an instance of AsynWebCrawler

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url = "https://crawl4ai.com")

        print(result.markdown)

asyncio.run(main())
