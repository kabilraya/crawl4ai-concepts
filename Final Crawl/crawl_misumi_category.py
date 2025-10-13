import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CacheMode, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
import re
from bs4 import BeautifulSoup #for better HTML Parser
from crawl4ai.deep_crawling import FilterChain, URLPatternFilter

async def website_crawling():

    #setting up the configs for crawling

    browser_config = BrowserConfig(verbose = True, headless = False)

    run_config = CrawlerRunConfig(
        word_count_threshold = 50, #a block(can be div or element) must contain atleast 50 words to be considered in the result
        markdown_generator = DefaultMarkdownGenerator(),
        excluded_tags = ["header", "nav", "footer" ,"aside","form" ,"script","style"],
        only_text=False,
        # target_elements = ["div"],
        # css_selector="div.card-product-linear"
        remove_forms = True,
        parser_type="lxml",
        
        #networking, caching configs

        disable_cache=False,
        no_cache_read = False,
        no_cache_write = False,
        method = "GET",
        check_robots_txt = False, #if true also considers the robot.txt provided by the site
        delay_before_return_html = 10.0 ,
        mean_delay = 2.0,
        max_range = 6.0,
        semaphore_count=5,
        js_code = """
            const read_more = document.querySelectorAll('a[data-spec="catchCopyRead"][data-read="more"]');
            read_more.forEach(link=>link.click());
            return true;
        """,
        scan_full_page = True,
        scroll_delay = 5.0,
        max_scroll_steps = 10,           
        process_iframes = True,
        simulate_user = True,
        remove_overlay_elements = True,
        

        exclude_social_media_domains = [],
        exclude_external_links = True,
        exclude_social_media_links = True,
        exclude_domains = [],
        # deep_crawl_strategy = BFSDeepCrawlStrategy(
        #     max_pages = 300,
        #     max_depth = 2,
        #     include_external = False


        
        verbose = True,
        log_console=False,
        capture_network_requests = False,
        capture_console_messages=False,
    )

    async with AsyncWebCrawler(config = browser_config) as crawler:
        results = await crawler.arun(url = "https://us.misumi-ec.com/vona2/mech/M0100000000/M0101000000/?curSearch=%7b%22field%22%3a%22%40search%2cseriesList.templateType%22%2c%22categoryCode%22%3a%22M0101000000%22%2c%22sort%22%3a1%2c%22allSpecFlag%22%3a0%2c%22page%22%3a1%2c%22brandModeFlag%22%3a1%2c%22pageSize%22%3a%2245%22%7d&listDisplay=mc-list",config = run_config, deep_crawl = False)

        if results:
            total = len(results)
            print(f"Total number of crawled webpages is {total}")

            with open("linear-shaft.md","w",encoding = "utf-8") as m, open("filtered_url.txt","w", encoding = "utf-8") as f:
                for i,result in enumerate(results,start=1):
                    if hasattr(result,"url") and result.url:
                        print(f"[{i}/{total}] Found: {result.url}")
                        f.write(result.url + "\n")
                    if hasattr(result,"html") and result.html:
                        html = result.html
                        soup = BeautifulSoup(html,"html.parser")
                        divs = soup.find_all("div",class_ = "m-panel")

                        content = ""
                        if divs:
                            for div in divs:
                                content+=str(div) + "\n\n end of a product \n\n"
                        else:
                            print(f"No div found in {result.url}")
                        print(f"Found {len(divs)} product divs in {result.url}")
                        m.write(content + "\n\n\n")
            print("Crawl Successfully completed")
        else:
            print(f"Crawl Failed")

asyncio.run(website_crawling())