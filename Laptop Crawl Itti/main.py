from internal_links_extract import crawl_for_internal_links
from laptop_information_extract import crawl_for_information
import asyncio
base_url = "https://itti.com.np/laptops-by-brands"
async def main():
    internal_links = await crawl_for_internal_links(base_url=base_url)
    await crawl_for_information(internal_links=internal_links)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
