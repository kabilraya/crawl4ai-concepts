import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
async def internal_links_extraction():
    """
    css selectors
    product_link = div.product-item-box>div.product-img-wrapper
    next_page_button = ul.page-numbers>li>a[data-ci-pagination-page="2"]:nth-of-type(1):not([rel="next"])
    """
    url = "https://www.neostore.com.np/product-category/laptop-brands"
    internal_links = []
    browser_config = BrowserConfig(headless = False, verbose = True)
    session_id = str(uuid.uuid4())
    
    async with AsyncWebCrawler(config = browser_config) as crawler:

        for page in range(1,6):
            if page == 1:

                run_conf = CrawlerRunConfig(
                    word_count_threshold = 10,
                    cache_mode=CacheMode.DISABLED,
                    scroll_delay=1.5,
                    delay_before_return_html=5.0,
                    
                    exclude_external_images=True,
                    exclude_domains=[],
                    exclude_social_media_domains=[],
                    exclude_social_media_links=True,
                    markdown_generator=DefaultMarkdownGenerator(),
                    css_selector="div.product-item-box>div.product-description>h3",
                    mean_delay = 3.0,
                    scan_full_page=True,
                    simulate_user=True,
                    process_iframes=True,
                    session_id = session_id,
                    only_text = False,
                    remove_overlay_elements = True,
                    check_robots_txt=False,
                    

                )
                print(f"Crawling page {page}")
                results = await crawler.arun(url = url,config = run_conf)
            else:
                print(f"Crawling page {page}")
                js_code_click = f"""
                document.querySelector('ul.page-numbers>li>a[data-ci-pagination-page="{page}"]:nth-of-type(1):not([rel="next"])').click();
                return true;
                """
                run_conf_two = CrawlerRunConfig(
                    word_count_threshold = 10,
                    cache_mode=CacheMode.DISABLED,
                    scroll_delay=1.5,
                    delay_before_return_html=15.0,
                    
                    exclude_external_images=True,
                    exclude_domains=[],
                    exclude_social_media_domains=[],
                    exclude_social_media_links=True,
                    markdown_generator=DefaultMarkdownGenerator(),
                    css_selector="div.product-item-box>div.product-description>h3",
                    mean_delay = 2.0,
                    js_code = js_code_click,
                    
                    simulate_user=True,
                    process_iframes=True,
                    session_id = session_id,
                    only_text = False,
                    remove_overlay_elements = True,
                    check_robots_txt=False,
                    js_only=True,
                    wait_for="css:div.product-item-box>div.product-description"
                )
                results = await crawler.arun(url = url, config = run_conf_two)
            if results.success:
                print("Crawling is successful")
                
            
                for link in results.links["internal"]:
                    internal_link = link.get("href")
                    if internal_link not in internal_links:
                        internal_links.append(internal_link)
            else:
                print("Crawling unsuccessful")
                break
        with open("internal-links.txt","a",encoding = "utf-8") as f:
            for int_link in internal_links:
                f.write(int_link + "\n")

asyncio.run(internal_links_extraction())



