from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import asyncio
import uuid
import json
import pandas as pd
async def json_css_product_extraction():
    session_id = str(uuid.uuid4())
    schema_one = {
        "name" : "part-number",
        "baseSelector":"div.PartNumberList_mainOuter__d74Qg>div.mergedRow",#tr.PartNumberColumn_dataRow__43D6Y
        "fields" : [
            {
            "name":"Product_Name",
            "selector" : "h1.PageHeading_wrap__K1c1n",
            "type" : "text",
            },
            {
                "name" : "Part Number",
                "selector":"tr.PartNumberColumn_dataRow__43D6Y div",
                "type" : "text"
            },
            {
                "name" : "URL",
                "selector":"https://vn.misumi-ec.com/" + "tr.PartNumberColumn_dataRow__43D6Y a",
                "type" : "attribute",
                "attribute" : "href"
            },
            {
                "name" : "Price",
                "selector":"tr.PartNumberAsideColumns_dataRow__OUw8N>td:nth-child(1)",
                "type" : "text",
            },
            {
                "name" : "Day_to_Ship",
                "selector":"tr.PartNumberAsideColumns_dataRow__OUw8N>td:nth-child(2)",
                "type" : "text",
            },
            {
                "name" : "Minimum Order Qty",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(1)",
                "type" : "text",
            },
            {
                "name" : "Volume Discount",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(2)",
                "type" : "text",
            },
            {
                "name" : "RoHS",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(3)",
                "type" : "text",
            },
            {
                "name" : "Outer Diameter(mm)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(4)",
                "type" : "text",
            },
            {
                "name" : "Width B(mm)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(5)",
                "type" : "text",
            },
            {
                "name" : "Stud Screw Nominal(M)(mm)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(6)",
                "type" : "text",
            },
            {
                "name" : "Roller Guiding Method",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(7)",
                "type" : "text",
            },
            {
                "name" : "Cam Follower: Stud Screw (Fine Thread)(mm)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(8)",
                "type" : "text",
            },
            {
                "name" : "Basic Load Rating Cr (Dynamic)(kN)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(9)",
                "type" : "text",
            },
            {
                "name" : "Basic Load Rating Cor (Static) (kN)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(10)",
                "type" : "text",
            },
            {
                "name" : "Allowable Rotational Speed (rpm)",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(11)",
                "type" : "text",
            },
            {
                "name" : "Seal",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(12)",
                "type" : "text",
            },
            {
                "name" : "Application",
                "selector":"tr.PartNumberSpecColumns_dataRow__M4B4a>td:nth-child(13)",
                "type" : "text",
            },
        ]
    }

    browser_config = BrowserConfig(headless = False, verbose = True, enable_stealth=True)
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        exclude_all_images=True,
        exclude_external_links=True,
        css_selector="h1.PageHeading_wrap__K1c1n,p.BasicInformation_catchCopy__h8mKx,div.PartNumberList_mainOuter__d74Qg",
        process_iframes=True,
        cache_mode=CacheMode.DISABLED,
        exclude_domains=[],
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        mean_delay=2.0,
        delay_before_return_html=60.0,
        extraction_strategy=JsonCssExtractionStrategy(schema=schema_one),
        markdown_generator=DefaultMarkdownGenerator(),
        js_code="""
            
            const langButton = document.querySelector('a[lang="en"]');
            if (langButton) langButton.click();

            
            
            setTimeout(() => {
                const partTab = document.querySelector('a#codeList');
                if (partTab) partTab.click();
                
            setTimeout(()=>{
            const partRows = document.querySelectorAll('tr.PartNumberColumn_dataRow__43D6Y');
            const priceRows = document.querySelectorAll('tr.PartNumberAsideColumns_dataRow__OUw8N');
            const specRows = document.querySelectorAll('tr.PartNumberSpecColumns_dataRow__M4B4a');

            
            
            const mainContainer = document.querySelector('div.PartNumberList_mainOuter__d74Qg');
            const mergedContainer = document.createElement('div');
            mergedContainer.classList.add('mergedRowContainer');
            const numRows = Math.min(partRows.length, priceRows.length, specRows.length);
            for (let i = 0; i < numRows; i++) {
            const row = document.createElement('div');
            row.classList.add('mergedRow');
            row.appendChild(partRows[i]);
            row.appendChild(priceRows[i]);
            row.appendChild(specRows[i]);
            mainContainer.appendChild(row)
            }
            },10000);
            }, 20000);
            
            
            
            return true;
        """,
        wait_for="css:div.Complex_attributesPanel__9800L",
        session_id=session_id,
        excluded_tags=["footer"],
        remove_forms=True,
        remove_overlay_elements=True
    )
    async with AsyncWebCrawler(config = browser_config) as crawler:
        result = await crawler.arun(url = "https://vn.misumi-ec.com/vona2/detail/221006228542?list=PageCategory",config = run_config)
        
        data = json.loads(result.extracted_content)
        print(data)
        print(len(data))
        df = pd.DataFrame(data)
        print(df)
        df.to_excel('misumi_products.xlsx', index=False)
asyncio.run(json_css_product_extraction())