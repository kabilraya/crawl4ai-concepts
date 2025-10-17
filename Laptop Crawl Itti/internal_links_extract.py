import asyncio
from crawl4ai import BrowserConfig, AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
async def crawl_for_internal_links(base_url):
    """
        url = https://itti.com.np/laptops-by-brands

        css-selectors
        for-product-links = div.product-grid-layout>div
        pagination:li.page-item>a[aria-label="Page 2"]
        
    """
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(verbose = True, headless = False)
    internal_links = []
    async with AsyncWebCrawler(config = browser_config) as crawler:
        for page in range(1,8):
            if(page == 1):
                results = await crawler.arun(url = base_url,config = CrawlerRunConfig(
                    word_count_threshold=2,
                    css_selector= "div.product-grid-layout>div>div>div>div:nth-child(2)",
                    exclude_domains=[],
                    excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
                    exclude_social_media_domains=[],
                    exclude_external_links=True,
                    exclude_social_media_links=True,
                    mean_delay = 5.0,
                    scan_full_page=True,
                    
                
                simulate_user = True,
                markdown_generator=DefaultMarkdownGenerator(),
                delay_before_return_html=15.0,
                session_id = session_id,
                cache_mode=CacheMode.DISABLED,
                scroll_delay=1.5
                ))
            else:
                results = await crawler.arun(url = f"{base_url}?page={page}",config = CrawlerRunConfig(
                    word_count_threshold = 2,
                    css_selector="div.product-grid-layout>div>div>div>div:nth-child(2)",
                    exclude_domains=[],
                    scroll_delay=1.5,
                    exclude_social_media_domains = [],
                    exclude_social_media_links = True,
                    exclude_external_links=True,
                    excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
                    mean_delay = 5.0,
                    scan_full_page = True,
                    delay_before_return_html=25.0,
                    simulate_user = True,
                    markdown_generator=DefaultMarkdownGenerator(),
                    session_id = session_id,
                    wait_for_timeout=120000,
                    cache_mode=CacheMode.DISABLED
                ))
            if results.success:
                for link in results.links["internal"]:
                    product_link = link.get("href")
                    if product_link not in internal_links:
                        internal_links.append(product_link)
            else:
                break;
        #writing in a file

        with open("internal-links.txt","a",encoding="utf-8") as f:
            for idx,internal_link in enumerate(internal_links):
                f.write(f"{idx} {internal_link}" + "\n")
        print(len(internal_links))
        return internal_links


