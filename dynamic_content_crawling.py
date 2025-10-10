
import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from crawl4ai import JsonCssExtractionStrategy
import json
async def dynamic_rendering_with_js():
    browser_config = BrowserConfig(headless = True,java_script_enabled = True)
    schema = {
        "name" : "KidoCodeCourse",
        "baseSelector":"div.body",
        "fields" : [
            {"name":"Documentaion-Title",
            "selector" : "h1",
            "type" : "text"
            },
            [
            {
                "name" : "links",
                "selector" : ".body>table.contentstable:nth-of-type(1)>tbody>tr>td>p.biglink>a.biglink",
                "type" : "attribute",
                "attribute" : "href"
            },
            ]
        ]
    }

    js_code = """
            (async()=>{
                const tabs = document.querySelectorAll("section.charge-methodology .tabs-menu-3 > div");
                for (let tab in tabs){
                    tab.scrollIntoView();
                    tab.click();
                    await new Promise(r=>setTimeout(r,5000))
                }
            })();
            """

    run_config = CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(
        schema=schema
        ),
        cache_mode=CacheMode.BYPASS, js_code=[js_code]
        )

    async with AsyncWebCrawler(config = browser_config) as crawler:
        result =await crawler.arun(url = "https://docs.python.org/3/",config = run_config)

        companies= json.loads(result.extracted_content)
        print(companies)
asyncio.run(dynamic_rendering_with_js())