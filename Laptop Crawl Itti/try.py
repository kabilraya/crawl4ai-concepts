import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid
from playwright_stealth import Stealth
async def crawl_for_information():
    
    browser_config = BrowserConfig(headless = False, verbose = True, enable_stealth=True)
    session_id =  str(uuid.uuid4())
    run_conf_first = CrawlerRunConfig(
        word_count_threshold = 20,
        exclude_domains=[],
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        markdown_generator=DefaultMarkdownGenerator(),
        css_selector=f"""div#__next>main>main>div>div:nth-child(2)>div:nth-child(2)>div:nth-child(4)>h1,
    div#__next>main>main>div>div:nth-child(2)>div:nth-child(2)>div:nth-child(4)>div:nth-child(4)>div,
    div#__next>main>main>div>div:nth-child(2)>div:nth-child(2)>div:nth-child(4)>div:nth-child(8),
    div#tab-id>div:nth-child(2) table
    """,
        excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
        delay_before_return_html=10.0,
        cache_mode=CacheMode.DISABLED,
        scan_full_page=True,
        method = "GET",
        check_robots_txt="False",
        only_text=False,
        mean_delay=3.0,
        scroll_delay = 3.0,
        process_iframes=True,
        session_id = session_id
    )
    wait_for_description_visible = "div#description-tab"
    run_conf_second = CrawlerRunConfig(
        word_count_threshold = 20,
        exclude_domains=[],
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        markdown_generator=DefaultMarkdownGenerator(),
        css_selector="div#description-tab div#specification-tab",
        excluded_tags=["header", "footer", "nav", "aside", "form", "script", "style"],
        delay_before_return_html=5.0,
        js_code = """
async function clickDescriptionButton() {
    return new Promise((resolve) => {
    const check = () => {
    const buttons = document.querySelectorAll("div#tab-id>div>button");
    if (buttons && buttons.length > 1) {
    
    buttons[1].click();
    resolve(true);
    } else {
        
        setTimeout(check, 500);
    }
    };
    check();
});
}
clickDescriptionButton();
""",
        # js_only=True,
        wait_for=f'css:div#description-tab div#specification-tab>h3',
        wait_for_timeout=100000,
        cache_mode=CacheMode.DISABLED,
        scan_full_page=True,
        method = "GET",
        check_robots_txt="False",
        only_text=False,
        mean_delay=3.0,
        scroll_delay = 3.0,
        process_iframes=True,
        session_id = session_id
    )

    async with AsyncWebCrawler(config = browser_config) as crawler:

        result_first_crawl = await crawler.arun(url = "https://itti.com.np/product/acer-predator-helios-neo-16s-2025-price-nepal-rtx-5060",config = run_conf_first)
        result_second_crawl = await crawler.arun(url="https://itti.com.np/product/acer-predator-helios-neo-16s-2025-price-nepal-rtx-5060",config = run_conf_second)
        if result_first_crawl.success and result_second_crawl.success:
            if result_second_crawl.markdown:
                print(result_first_crawl.markdown + "\n" + result_second_crawl.markdown)

asyncio.run(crawl_for_information())