import asyncio
from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
async def internal_links_extraction():
    browser_config = BrowserConfig(headless = False, verbose = True)
    internal_links = []
    session_id = str(uuid.uuid4())
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for i in range(1,6):
            if i == 1:
                run_config = CrawlerRunConfig(
                    word_count_threshold=10,
                    cache_mode=CacheMode.DISABLED,
                    exclude_domains=[],
                    exclude_social_media_domains=[],
                    exclude_external_links=True,
                    exclude_social_media_links=True,
                    css_selector="div.product-item-info>a",
                    scroll_delay=1.5,
                    delay_before_return_html=5.0,
                    scan_full_page=True,
                    simulate_user = True,
                    process_iframes=True,
                    
                    only_text = False,
                    check_robots_txt=False,
                    markdown_generator=DefaultMarkdownGenerator(),
                    exclude_all_images=True,
                    session_id=session_id,
                )
                result = await crawler.arun(url = "https://dealayo.com/laptops.html", config = run_config)
            else:
                run_config = CrawlerRunConfig(
                    word_count_threshold=20,
                    cache_mode = CacheMode.DISABLED,
                    exclude_domains=[],
                    exclude_social_media_domains=[],
                    exclude_external_links=True,
                    exclude_social_media_links=True,
                    scroll_delay=1.5,
                    delay_before_return_html=5.0,
                    css_selector = "div.product-item-info>a",
                    excluded_tags = ["header","footer","nav","aside","form","script","style"],
                    js_code = f"""
                        document.querySelector('a.page[href="https://dealayo.com/laptops.html?p={i}"]').click();
                        return true;
                """,
                
                    scan_full_page=True,
                    simulate_user = True,
                    process_iframes=True,
                    session_id = session_id,
                    only_text = False,
                    js_only=True,
                    check_robots_txt=False,
                    markdown_generator=DefaultMarkdownGenerator(),
                    exclude_all_images=True
                )
                result = await crawler.arun(url ="https://dealayo.com/laptops.html", config = run_config)
            if result.success:
                print(f"Crawling for page {i} was successfull")

                for link in result.links["internal"]:
                    internal_link = link.get("href")
                    if internal_link not in internal_links:
                        internal_links.append(internal_link)
            else:
                print("Crawling not successful")
                break
    with open("internal-links.txt","a",encoding = "utf-8") as f:
        for internal_link in internal_links:
            f.write(internal_link + "\n")
    return internal_links
