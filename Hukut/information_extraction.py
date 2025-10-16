import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode,BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
#product_price = section:nth-of-type(1)>section>div:nth-child(2)>div:nth-child(2)
#for extending the description of the product: svg.chevron
#overview = div.overview
#specs = section#specs>div>div>div
async def crawl_for_information(internal_links):
    browser_config = BrowserConfig(verbose = True, headless = True)
    run_conf = CrawlerRunConfig(
        
    css_selector="section:nth-of-type(1)>section>div:nth-child(2)>div:nth-child(2),div.overview,section#specs",
    word_count_threshold=10,  
        
    excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
    markdown_generator=DefaultMarkdownGenerator(),
    cache_mode=CacheMode.DISABLED,
    delay_before_return_html=20.0,
    js_code=""" 
    window.scrollTo(0, document.body.scrollHeight);
    const buttons = document.querySelectorAll("h3>button");
    for (const button of buttons){
        button.click();
    }
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
            for link in internal_links:
                results = await crawler.arun(url = link,config = run_conf)
                if results.success:
                    print(results.markdown)

                    with open("info.md","a",encoding="utf-8") as f:
                        f.write(results.markdown + "\n\n\n\n---------End of the Product---------\n\n\n\n")
    
