import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url ="https://example.com")
        print(result.markdown) #prints 300 first characters

asyncio.run(main())