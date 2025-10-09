import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig,CrawlerRunConfig,CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
async def crawl():
    browser_config = BrowserConfig(headless = False) #False for Ui of crawl(browser rendering) and True for no UI
    
    
    md_generator = DefaultMarkdownGenerator(content_filter=PruningContentFilter(threshold = 0.4, threshold_type = "fixed"))
    #this creates a default markdown without any content filter and also with content filter so we have 
    #two markdowns

    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS,markdown_generator = md_generator)
    async with AsyncWebCrawler(config = browser_config) as crawler:
        result = await crawler.arun(url = "https://news.ycombinator.com",config = run_config) 

        print(len(result.markdown.raw_markdown))
        print(len(result.markdown.fit_markdown))
        #.markdown just converts the html output of this form
        #CrawlResultContainer([CrawlResult(url='https://example.com', html='<!DOCTYPE html><html><head>\n    
        # <title>Example Domain</title>\n\n    <meta charset="utf-8">\n    
        # <meta http-equiv="Content-type" content="text/html; charset=utf-8">\n    
        # <meta name="viewport" content="width=device-width, initial-scale=1">\n    
        # <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n
        #font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, 
        # sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        
        # margin: 5em auto;\n

        # to this form 
        #This domain is for use in illustrative examples in documents. You may use this domain 
        # in literature without prior coordination or asking for permission.        
        #[More information...](https://www.iana.org/domains/example)

asyncio.run(crawl())