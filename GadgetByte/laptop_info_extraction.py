from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from internal_links_extraction import extract_internal_links
import asyncio

"""

div.title-toolbar>h1
div.woocommerce-product-details__short-description
div.price
div.text-content.shown-all > :not(:first-child)
button.btn
div#section-description>div.specification-accordion>:not(:nth-child(2)) table
div#section-description>div.specification-accordion>:not(:nth-child(2)) h2
"""
async def laptop_information_extract():
    internal_links = await extract_internal_links()
    browser_config = BrowserConfig(headless = True,verbose = True,enable_stealth=True)
    run_conf = CrawlerRunConfig(
        css_selector="div.title-toolbar>h1,div.woocommerce-product-details__short-description,div.price,div.text-content.shown-all > :not(:first-child)div#section-description>div.specification-accordion>:not(:nth-child(2)) h2,div#section-description>div.specification-accordion>:not(:nth-child(2)) table",
        word_count_threshold=10,
        exclude_all_images=True,
        exclude_domains=[],
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        simulate_user=True,
        scroll_delay=1.5,
        mean_delay=1.5,
        scan_full_page=True,
        exclude_internal_links=True,
        remove_overlay_elements=True,
        excluded_tags=["nav","header","footer","img","a"],
        markdown_generator=DefaultMarkdownGenerator(),
        js_code="""
            document.querySelector('button.btn').click();
            return true;
        """,
        delay_before_return_html=10.0,

    )
    async with AsyncWebCrawler(config = browser_config) as crawler:
        for link in internal_links:
            results = await crawler.arun(url = link,config = run_conf)

            if results.success:
                print(results.markdown)
                with open("gadget-byte-laptop.md","a",encoding="utf-8") as f:
                    f.write(f'{results.markdown}  \n\n URL: {link} \n\n\n-----End of Product-----\n\n\n')

asyncio.run(laptop_information_extract())