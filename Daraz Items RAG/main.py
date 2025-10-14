
import asyncio
from each_item_crawl import each_item_crawl
from internal_links_extraction import crawling_for_product_links
if __name__ == "__main__":
    list_of_links = asyncio.run(crawling_for_product_links(website_url="https://www.daraz.com.np/apple/?q=mobile%20phones"))
    results = asyncio.run(each_item_crawl(list_of_links=list_of_links))
    