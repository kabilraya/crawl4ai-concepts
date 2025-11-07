from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig,LLMConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import asyncio
import uuid
import json
import pandas as pd
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re

async def json_css_product_extraction():
    load_dotenv()
    base_url = "https://vn.misumi-ec.com/vona2/detail/110302715510?list=PageCategory"
    api_key = os.getenv("GOOGLE_API_KEY")  
    session_id = str(uuid.uuid4())
    query = "Generate a schema to extract product details.The column names from the tables MUST exact. Only use the table column names as the key_fields in the json schema(Split the Part Number header into two keys - Part Number Name and Part Number URL)  You MUST use CSS selectors, not XPath. The base selector should be 'div.mergedRow'."
    initial_run_config = CrawlerRunConfig(
            delay_before_return_html=30.0,
            js_code="""
                setTimeout(()=>{
                const langButton = document.querySelector('a[lang="en"]');
                if (langButton) langButton.click();
                },3000)
                
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
            },5000);
            }, 10000);
            """,
            wait_for="css:div.PartNumberList_mainOuter__d74Qg"
        )
    # initial_result = await crawler.arun(url="https://vn.misumi-ec.com/vona2/detail/221006228542?list=PageCategory", config=initial_run_config)
    
    
    browser_config = BrowserConfig(headless = False, verbose = True, enable_stealth=True)
    sub_category = ""
    async with AsyncWebCrawler(config = browser_config) as crawler:
        initial_result = await crawler.arun(url=base_url, config=initial_run_config)        
        soup = BeautifulSoup(initial_result.html, "html.parser")
        
        table_container = soup.select_one("div.PartNumberList_mainOuter__d74Qg")
        title_element = soup.select_one("h1.PageHeading_wrap__K1c1n")
        sub_category = title_element.get_text(strip=True) if title_element else "unknown_product" 
        cleaned_html = str(table_container)
        css_schema = JsonCssExtractionStrategy.generate_schema(
        html=cleaned_html,
        schema_type="css", 
        query=query,
        llm_config = LLMConfig(provider="gemini/gemini-2.5-flash",api_token=api_key)
    )
        print(css_schema)
        
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
        extraction_strategy=JsonCssExtractionStrategy(schema=css_schema),
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
        result = await crawler.arun(url = base_url,config = run_config)

        
        data = json.loads(result.extracted_content)
        print(data)
        print(len(data))
        df = pd.DataFrame(data)
        print(df)
        sub_category = re.sub(r'[ ,]+', '_', sub_category)
        file_name = f"camfollower_{sub_category}.xlsx".lower()
        
        df.to_excel(file_name, index=False)
asyncio.run(json_css_product_extraction())