import asyncio
from internal_links_extraction import internal_links_extraction
from laptop_information_crawl import crawl_for_information
base_url = "https://www.neostore.com.np/product-category/laptop-brands"
async def main():
    internal_links = await internal_links_extraction(base_url=base_url)
    await crawl_for_information(internal_links=internal_links)

if __name__ == "__main__":
    asyncio.run(main())