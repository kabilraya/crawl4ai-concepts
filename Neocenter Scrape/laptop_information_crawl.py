import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
async def crawl_for_information(internal_links):
    """
    h1.product_title 
    div.woocommerce-product-details__short-description>ul
    ins>span.amount:nth-of-type(1)>bdi:nth-child(1)
    a[href="#tab-specification"]
    div.woocommerce-tabs>div.woocommerce-Tabs-panel:nth-child(3)>table
    """
    browser_config = BrowserConfig(headless = True, verbose = True)
    session_id =  str(uuid.uuid4())
    run_conf_first = CrawlerRunConfig(
        word_count_threshold = 5,
        exclude_domains=[],
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        markdown_generator=DefaultMarkdownGenerator(),
        css_selector="h1.product_title ,div.woocommerce-product-details__short-description>ul,ins>span.amount:nth-of-type(1)>bdi:nth-child(1)",
        excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
        delay_before_return_html=10.0,
        cache_mode=CacheMode.DISABLED,
        scan_full_page=True,
        method = "GET",
        check_robots_txt="False",
        only_text=False,
        mean_delay=3.0,
        scroll_delay = 3.0,
        process_iframes=True,
        session_id = session_id
    )

    run_conf_second = CrawlerRunConfig(
        word_count_threshold = 5,
        exclude_domains=[],
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        markdown_generator=DefaultMarkdownGenerator(),
        css_selector="div#tab-specification > table",
        excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
        delay_before_return_html=10.0,
        js_code = """
        document.querySelector('a[href="#tab-specification"]').click()
        return true;
        """,
        js_only=True,
        wait_for="css:div#tab-specification > table",
        cache_mode=CacheMode.DISABLED,
        scan_full_page=True,
        method = "GET",
        check_robots_txt="False",
        only_text=False,
        mean_delay=3.0,
        scroll_delay = 3.0,
        process_iframes=True,
        session_id = session_id
    )

    async with AsyncWebCrawler(config = browser_config) as crawler:
        for internal_link in internal_links:
            result_first_crawl = await crawler.arun(url = internal_link,config = run_conf_first)
            result_second_crawl = await crawler.arun(url=internal_link,config = run_conf_second)
            if result_first_crawl.success and result_second_crawl.success:

                print(result_first_crawl.markdown + "\n" + result_second_crawl.markdown)
                with open("neo-laptops-info.md","a",encoding="utf-8") as f:
                    f.write(f'{result_first_crawl.markdown} \n {result_second_crawl.markdown} \n URL: {internal_link} \n\n\n\n------End of the Product------\n\n\n\n')

        
            