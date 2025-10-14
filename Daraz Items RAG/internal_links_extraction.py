import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CacheMode, BrowserConfig, CrawlerRunConfig
from crawl4ai.deep_crawling import DeepCrawlStrategy, BFSDeepCrawlStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import re
from bs4 import BeautifulSoup

async def crawling_for_product_links():
    browser_config = BrowserConfig(headless = True, verbose = True)

    run_conf = CrawlerRunConfig(
        word_count_threshold=50,
        markdown_generator = DefaultMarkdownGenerator(),
        excluded_tags = ["header","nav","footer","aside","form","script","style"],
        only_text = False,
        remove_forms = True,
        parser_type = "lxml",

        disable_cache = False,
        no_cache_read = False,
        no_cache_write = False,
        method = "GET",
        check_robots_txt = False,
        delay_before_return_html = 10.0,
        mean_delay = 2.0,
        max_range = 6.0,
        semaphore_count= 5,
        js_code=""" 
        window.scrollTo(0,document.body.scrollHeight);
        return true;
        """,
        scan_full_page = True,
        scroll_delay = 1.5,
        max_scroll_steps = 3,
        process_iframes = True,
        remove_overlay_elements=True,
        simulate_user = True,

        exclude_social_media_domains = [],
        exclude_external_links=True,
        exclude_social_media_links = True,
        exclude_domains = [],
        css_selector=".Ms6aG",
        target_elements = ['div'], 

        verbose = True,
        capture_console_messages=False,
        capture_network_requests=False,
    )

    async with AsyncWebCrawler(config = browser_config) as crawler:
        results = await crawler.arun(url = "https://www.daraz.com.np/car-mounts/?up_id=480819836&clickTrackInfo=matchType--20___description--17%2525%2Boff___seedItemMatchType--c2i___bucket--0___spm_id--category.hp___seedItemScore--0.0___abId--379344___score--0.1___pvid--9069c3b8-8e56-498c-b407-1a79b8173c12___refer--___appId--7253___seedItemId--480819836___scm--1007.17253.379344.0___categoryId--9540___timestamp--1760351635479&from=hp_categories&item_id=480819836&version=v2&q=car%2Bmounts&params=%7B%22catIdLv1%22%3A%222%22%2C%22pvid%22%3A%229069c3b8-8e56-498c-b407-1a79b8173c12%22%2C%22src%22%3A%22ald%22%2C%22categoryName%22%3A%22Car%2BMounts%22%2C%22categoryId%22%3A%229540%22%7D&src=hp_categories&spm=a2a0e.tm80335409.categoriesPC.d_3_9540",config = run_conf)

        if results.success:
            #extracting all the internal links
            internal_links = []
            for result in results:
                for link in result.links["internal"]:
                    print(link)
                    url = link.get("href")
                    print(url)
                    internal_links.append(url+ "\n")
                    with open("product_links.txt",'a',encoding = "utf-8") as f:
                        f.write(url+"\n")

asyncio.run(crawling_for_product_links())