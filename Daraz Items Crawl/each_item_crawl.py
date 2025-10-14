import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig,CacheMode
from crawl4ai.user_agent_generator import UserAgent
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from clean_with_parser import parse_html_result
async def each_item_crawl(list_of_links):
    
    browser_config = BrowserConfig(headless=True, verbose=True)

    
    run_conf = CrawlerRunConfig(
        
        css_selector="div.pdp-block__product-detail, article.lzd-article,div.pdp-mod-specification, img.gallery-preview-panel",
        
        
        word_count_threshold=10,  
        
        excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
        markdown_generator=None,
        cache_mode=CacheMode.DISABLED,
        delay_before_return_html=20.0,
        js_code=""" 
        window.scrollTo(0, document.body.scrollHeight);
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

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for link in list_of_links:
            # url = "https://www.daraz.com.np/products/generic-universal-360-degree-long-neck-car-mount-phone-holder-with-strong-abs-silicon-base-i151662335.html"
            results = await crawler.arun(url=link, config=run_conf)
            if results.success:
                if results.html:
                    print("HTML exists")
                else:
                    print("Doesnt Exist")
            with open("raw-markdown.md","a",encoding="utf-8") as f:
                f.write(results.markdown + "\n\n\n ---End of Product--- \n\n\n")

            parse_html_result(result=results)