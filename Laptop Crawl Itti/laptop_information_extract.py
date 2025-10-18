import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode,BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
async def crawl_for_information(internal_links):

    """
    js_selector = div#tab-id>div:nth-child(1)>button
    """
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(verbose = True, headless = True)
    run_conf_one = CrawlerRunConfig(
    session_id=session_id,   
    css_selector=f"""div#__next>main>main>div>div:nth-child(2)>div:nth-child(2)>div:nth-child(4)>h1,
    div#__next>main>main>div>div:nth-child(2)>div:nth-child(2)>div:nth-child(4)>div:nth-child(4)>div,
    div#__next>main>main>div>div:nth-child(2)>div:nth-child(2)>div:nth-child(4)>div:nth-child(8),
    div#tab-id>div:nth-child(2) table
    """,
    word_count_threshold=10,  
        
    excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
    markdown_generator=DefaultMarkdownGenerator(),
    cache_mode=CacheMode.DISABLED,
    delay_before_return_html=20.0,
    js_code=""" 
    window.scrollTo(document.body.scrollHeight);
    return true;
        """,
        scan_full_page=True,
        remove_overlay_elements=True,
        simulate_user=True,
        verbose=True,
        method = "GET",
        check_robots_txt="False",
        only_text=False,
        mean_delay=3.0,
        scroll_delay = 3.0,
        process_iframes=True,
        
    )
    

    async with AsyncWebCrawler(config = browser_config) as crawler:
            for internal_link in internal_links:
                results_one = await crawler.arun(url =internal_link , config = run_conf_one)
                if results_one.success:
                    print(results_one.markdown)

                    with open("laptop-info.md","a",encoding="utf-8") as f:
                        f.write(f'{results_one.markdown}"\n"{internal_link}"\n\n\n------End the Product------\n\n\n"')

                
