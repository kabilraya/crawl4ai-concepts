import asyncio
from crawl4ai import LLMExtractionStrategy, AsyncWebCrawler, CacheMode, BrowserConfig,CrawlerRunConfig,LLMConfig
from pydantic import BaseModel,Field #this is used to tell the LLM what data or field in the page to look for while crawling
#inherits the BaseModel class in a user defined class
from typing import Dict
class OpenAiModelFee(BaseModel): #this is data model where all the data after the web crawling is stored
    #we define all the important Fields that must be extracted by the LLM for data representation  
    model_name:str = Field(...,description="This is the model name from the pricing page")
    input_fee:str = Field(...,description="This is the cost of input token")
    output_fee: str = Field(...,description= "This is the cost of output per token") #here the model_name,input_fee and the output_fee
    #are user defined.
    #after crawling the html page is provided to LLM with a prompt saying to extract info according to this fields and make a json

async def LLM_extraction_strategy(provider:str,api_token:str = None,extra_headers:Dict[str,str]=None):
    #Dict[str,str] -> of type dictionary with key=str and value=str
    if api_token is None and provider != "ollama/gemma3:1b-it-qat":
        print("Error! needs a api_token for the extraction process")
        return

    extra_args = {"temperature":0, "max_tokens":2000, "top_p":0.9}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    browser_config = BrowserConfig(headless = True)
    crawler_conf = CrawlerRunConfig(
        cache_mode = CacheMode.BYPASS,
        word_count_threshold = 1,
        page_timeout = 80000,
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider = provider,api_token=api_token),
            schema = OpenAiModelFee.model_json_schema(),
            extraction_type = "schema",
            instruction="""From the crawled content extract all the fields mentioned in the given BaseModel and provide a json format 
            with the particular schema mentioned.""",
            extra_args = extra_args
        )
    )
    async with AsyncWebCrawler(config = browser_config) as crawler:

        result  = await crawler.arun(url = "https://openai.com/api/pricing/", config=crawler_conf)

        print(result.extracted_content)

asyncio.run(LLM_extraction_strategy("ollama/gemma3:1b-it-qat"))
