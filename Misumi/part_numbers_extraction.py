# div.PartNumberList_mainOuter__d74Qg
#this is the table extraction
"""
div.PartNumberList_mainOuter__d74Qg
li.DetailTab_item__vonZh:nth-of-type(2):button for toggling to the part-numbers
div.Pagination_container__VOa4I:nth-of-type(1) li:nth-of-type(2) > a[href = "?Page=2"]:nth-child(1)- to change the page in the part-numbers table
div.PartNumberList_mainOuter__d74Qg
"""

import asyncio
from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid

async def part_numbers_extraction():
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(headless = False,verbose = True,enable_stealth=True)
    run_conf_one = CrawlerRunConfig(
        mean_delay=2.0,
        
        # scan_full_page=True,
        wait_for = "css:div.Complex_attributesPanel__9800L",
        js_code="""
            
            const langButton = document.querySelector('a[lang="en"]');
            if (langButton) langButton.click();

            
            setTimeout(() => {
                const partTab = document.querySelector('a#codeList');
                if (partTab) partTab.click();
            }, 20000);

            return true;
        """,
        delay_before_return_html=25.0,
        css_selector = "h1.PageHeading_wrap__K1c1n,p.BasicInformation_catchCopy__h8mKx,div.PartNumberList_mainOuter__d74Qg",
        markdown_generator=DefaultMarkdownGenerator(),
        process_iframes=True,
        simulate_user=True,
        exclude_all_images=True,
        exclude_domains=[],
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        exclude_external_images=True,
        exclude_internal_links=True,
        cache_mode=CacheMode.DISABLED,
        session_id=session_id,
        excluded_tags=["footer"]
        
    )
    
    async with AsyncWebCrawler(config = browser_config) as crawler:
        results_one = await crawler.arun(url = "https://vn.misumi-ec.com/vona2/detail/110300110020?list=PageCategory",config = run_conf_one)
        if results_one.success:
            print(results_one.markdown)
asyncio.run(part_numbers_extraction())