from clean_with_parser import parse_html_result
import asyncio
from each_item_crawl import each_item_crawl

if __name__ == "__main__":
    results = asyncio.run(each_item_crawl())

    parse_html_result(results)