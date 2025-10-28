import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator
from internal_links_extract import internal_links_extraction
import uuid
"""
h1.page-title
div.mobile_data>div.mobile_desc
js = div#tab-label-additional>a.data.switch
div#additional
span.price
"""
async def laptop_information_extraction():
    link = "https://dealayo.com/asus-e410-10th-gen-intel-celeron-4-256-gb-14-screen-laptop-white.html"
    session_id = str(uuid.uuid4())
    
    browser_config = BrowserConfig(verbose = True,headless = False )
    run_config_one = CrawlerRunConfig(
        word_count_threshold=10,
                    cache_mode=CacheMode.DISABLED,
                    exclude_domains=[],
                    exclude_social_media_domains=[],
                    exclude_external_links=True,
                    exclude_social_media_links=True,
                    css_selector="h1.page-title,span.price,div.mobile_data>div.mobile_desc",
                    scroll_delay=1.5,
                    delay_before_return_html=5.0,
                    scan_full_page=True,
                    simulate_user = True,
                    process_iframes=True,
                    session_id = session_id,
                    only_text = False,
                    check_robots_txt=False,
                    markdown_generator=DefaultMarkdownGenerator()
    )
    run_config_two = CrawlerRunConfig(
        word_count_threshold=10,
                    cache_mode=CacheMode.DISABLED,
                    exclude_domains=[],
                    exclude_social_media_domains=[],
                    exclude_external_links=True,
                    exclude_social_media_links=True,
                    css_selector="div#additional",
                    scroll_delay=1.5,
                    session_id = session_id,
                    delay_before_return_html=5.0,
                    scan_full_page=True,
                    simulate_user = True,
                    process_iframes=True,
                    js_code = f"""
                        document.querySelector('div#tab-label-additional>a.data.switch').click();
                        return true;
                    """,
                    js_only=True,
                    only_text = False,
                    check_robots_txt=False,
                    markdown_generator=DefaultMarkdownGenerator()
    )
    async with AsyncWebCrawler(config = browser_config) as crawler:
        
            result_one = await crawler.arun(url = link,config = run_config_one)
            result_two = await crawler.arun(url = link, config = run_config_two)

            if result_one.success and result_two.success:
                    print(f'{result_one.markdown} \n {result_two.markdown}')
                    with open("laptop-info-dealayo.md", "a" , encoding = "utf-8") as f:
                        f.write(f'{result_one.markdown} \n\n {result_two.markdown} \n\n URL:{link} \n\n -----End of the Product------\n\n')

asyncio.run(laptop_information_extraction())