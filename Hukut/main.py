from information_extraction import crawl_for_information
from internal_links_collection import crawl_product_links_with_pagination
import asyncio

async def main():
    url = "https://hukut.com/mobile-phones"
    #paste any link from hukut here. make it such that the url is the base of category of any product. for example mobile phones
    internal_links = await crawl_product_links_with_pagination(url)
    await crawl_for_information(internal_links=internal_links)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")


