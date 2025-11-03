from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
import asyncio


async def extract_internal_links():
    """
    css_selectors:
    product_div: div.RfADt>a
    pagination : div.e5J1n li[title="1"]
    """
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(headless=True, verbose=True, enable_stealth=True)
    internal_links = []

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for i in range(1, 5):
            if i == 1:
                run_conf = CrawlerRunConfig(
                    word_count_threshold=10,
                    css_selector="div.RfADt>a",
                    cache_mode=CacheMode.DISABLED,
                    exclude_all_images=True,
                    exclude_domains=[],
                    exclude_external_links=True,
                    simulate_user=True,
                    delay_before_return_html=5.0,
                    mean_delay=2.5,
                    scan_full_page=True,
                    exclude_social_media_domains=[],
                    exclude_social_media_links=True,
                    session_id=session_id,
                    scroll_delay=1.0,
                )

                result = await crawler.arun(
                    url="https://www.daraz.com.np/catalog/?spm=a2a0e.searchlist.cate_6.5.6abb17f6fPy9OR&q=Smartphones&from=hp_categories&src=all_channel",
                    config=run_conf,
                )

            else:
                run_conf = CrawlerRunConfig(
                    word_count_threshold=10,
                    css_selector="div.RfADt>a",
                    cache_mode=CacheMode.DISABLED,
                    exclude_all_images=True,
                    exclude_domains=[],
                    exclude_external_links=True,
                    simulate_user=True,
                    delay_before_return_html=10.0,
                    mean_delay=2.5,
                    scan_full_page=True,
                    exclude_social_media_domains=[],
                    exclude_social_media_links=True,
                    session_id=session_id,
                    scroll_delay=1.0,
                    js_code=f"""
                        async function clickPageButton() {{
                            return new Promise((resolve) => {{
                                const check = () => {{
                                    const page = document.querySelector('div.e5J1n li[title="{i}"]');
                                    if (page) {{
                                        page.click();
                                        resolve(true);
                                    }} else {{
                                        setTimeout(check, 500);
                                    }}
                                }};
                                check();
                            }});
                        }}
                        clickPageButton();
                    """,
                    js_only=True,
                )

                result = await crawler.arun(
                    url="https://www.daraz.com.np/catalog/?spm=a2a0e.searchlist.cate_6.5.6abb17f6fPy9OR&q=Smartphones&from=hp_categories&src=all_channel",
                    config=run_conf,
                )

            if result.success:
                new_links_found = 0
                for link in result.links["internal"]:
                    url = link.get("href")
                    if url and url not in internal_links:
                        internal_links.append(url)
                        new_links_found+=1
                    print(new_links_found)

        with open("internal_links.txt", "a", encoding="utf-8") as f:
            for link in internal_links:
                f.write(link + "\n")
        return internal_links



