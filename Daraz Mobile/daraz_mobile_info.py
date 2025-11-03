from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import asyncio
from internal_links_extraction import extract_internal_links
async def information_extraction():
    browser_config = BrowserConfig(headless = True, verbose=True, enable_stealth=True)
    """
    css_selectors: 
    h1.pdp-mod-product-badge-title
    span.pdp-price
    div#module_product_detail>div 
    button.pdp-view-more-btn
    """
    # internal_links = await extract_internal_links()
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        simulate_user=True,
        js_code=f"""
                        async function clickMoreButton() {{
                            return new Promise((resolve) => {{
                                const check = () => {{
                                    const button = document.querySelector('button.pdp-view-more-btn');
                                    if (button) {{
                                        button.click();
                                        resolve(true);
                                    }} else {{
                                        setTimeout(check, 500);
                                    }}
                                }};
                                check();
                            }});
                        }}
                        clickMoreButton();
                    """,
        css_selector="h1.pdp-mod-product-badge-title, div.pdp-product-price>span, div.pdp-product-highlights,ul.specification-keys",
        exclude_domains=[],
        exclude_all_images=True,
        excluded_tags=["nav","header","footer","img"],
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        delay_before_return_html=20.0,
        mean_delay=2.0,
        scroll_delay=1.5,
        markdown_generator=DefaultMarkdownGenerator(),
        cache_mode=CacheMode.DISABLED,
        check_robots_txt=False,
        scan_full_page=True

    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
            link = "https://www.daraz.com.np/products/vivo-y29-8256-gb-l-6500mah-battery-with-44w-fast-charger-l-50mp2mp-front-camera-8mp-l-andriod-14-i409077474.html"
            result = await crawler.arun(url = link,config=run_config)
            print(result.markdown)
            with open("daraz_mobile.md","a",encoding="utf-8") as f:
                f.write(f'{result.markdown} \n URL: {link} \n---End of Product---\n')

asyncio.run(information_extraction())
