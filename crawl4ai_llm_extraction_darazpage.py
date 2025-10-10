import json
import asyncio
from typing import Dict, List
from crawl4ai import LLMExtractionStrategy,LLMConfig,AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from pydantic import BaseModel,Field


class Product(BaseModel):
    product_name: str = Field(..., description="The full name or title of the product.")
    price: int = Field(..., description="The numeric price of the product. Currency symbols and commas must be removed.")



async def daraz_items_list(provider:str, api_token:str = None):
    
    if api_token is None and "ollama" not in provider:
        print("Error! API token is required for non-local providers.")
        return

    extra_args = {"temperature": 0, "top_p": 0.9}

    
    instruction = """
    You are an expert web scraping agent. Your task is to analyze the provided HTML content of a Daraz product listing page and extract specific information.

    
    1.  **Extract Details for Each Product:** For every product you find, extract the following:
        - The full `product_name` from the product div.
        - The `price` from the same product div. look for the class name for proper parent element.
    """

    browser_config = BrowserConfig(headless=True) 
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        page_timeout=120000,
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider=provider, api_token=api_token),
            schema=Product.model_json_schema(),
            extraction_type="schema",
            instruction=instruction,
            extra_args=extra_args
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url="https://www.daraz.com.np/measuring-levelling/?from=suggest_normal&q=camera", config=crawler_config)
        
        if result.extracted_content:
            try:
                
                data = json.loads(result.extracted_content)
                print(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                print("LLM returned invalid JSON. The output was:")
                print(result.extracted_content)
        else:
            print("Failed to extract any content. The LLM may have failed or timed out.")


asyncio.run(daraz_items_list("ollama/gemma3:1b-it-qat"))