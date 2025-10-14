import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def each_item_crawl():
    # Browser configuration remains the same
    browser_config = BrowserConfig(headless=False, verbose=True)

    
    run_conf = CrawlerRunConfig(
        
        css_selector="img.gallery-preview-panel, div.pdp-block__product-detail, article.lzd-article,div.pdp-mod-specification",
        
        word_count_threshold=20,  
        
        excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
        
        
        delay_before_return_html=5.0,
        js_code=""" 
        window.scrollTo(0, document.body.scrollHeight);
        return true;
        """,
        scan_full_page=True,
        remove_overlay_elements=True,
        simulate_user=True,
        verbose=True
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        url = "https://www.daraz.com.np/products/generic-universal-360-degree-long-neck-car-mount-phone-holder-with-strong-abs-silicon-base-i151662335.html"
        results = await crawler.arun(url=url, config=run_conf)

        if results.success:
            print("--- CRAWLED MARKDOWN ---")
            print(results.markdown)

            
            with open("product-details.md", "w", encoding="utf-8") as f:
                f.write(results.markdown)
            print("\n--- Successfully saved to product-details.md ---")
        else:
            print(f"Failed to crawl the page. Error: {results.error_message}")
    return results