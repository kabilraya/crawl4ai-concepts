from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
import asyncio


async def extract_internal_links():
    """
    css_selectors:
    product_div: div.title-star-wrap>a
    load_more_button : div.loadmorebtn-wrap>a
    """
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(headless=True, verbose=True, enable_stealth=True)
    internal_links = []

    async with AsyncWebCrawler(config=browser_config) as crawler:
        run_conf = CrawlerRunConfig(
                    word_count_threshold=10,
                    css_selector="div.title-star-wrap>a",
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
                    scroll_delay=1.5,
                    js_code="""
                async function clickViewButton(times = 7, delay = 5000) {
                    for (let i = 0; i < times; i++) {
                        let button = document.querySelector('div.loadmorebtn-wrap > a');
                        if (!button) {
                            break;
                        }
                        button.click();
                        await new Promise(r => setTimeout(r, delay)); // wait for the content to load properly 5 sec
                    }
                    return true;
                }
                return await clickViewButton();
            """,
        )

        result = await crawler.arun(
                url="https://www.gadgetbytenepal.com/cat/mobiles/",
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



