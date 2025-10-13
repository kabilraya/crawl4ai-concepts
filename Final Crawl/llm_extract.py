import os
import json
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import List, Dict
from markdownify import markdownify as md

load_dotenv()

api_token = os.getenv("GEMINI_API_KEY")

if not api_token:
    raise ValueError("Token not set")

client= genai.Client(api_key = api_token)

def llm_process():
    try:
        with open("linear-shaft.md","r",encoding="utf-8") as m:
            markdown_data = m.read()
    except FileNotFoundError:
        print("File not found")
        exit()
    
    products = [p.strip() for p in markdown_data.strip().split("\n\nend of a product\n\n") if p.strip()]

    for product in products:
        print(product)
    
    OUTPUT_FILE_NAME = "linear-shaft.json"
    PRODCUT_DELIMETER = "---PRODUCT-SEPARATOR---"
    all_product_markdowns = PRODCUT_DELIMETER.join(md(p) for p in products)
    
    prompt = f""" 
        You are an expert product data extraction system.
        Each product record is separated by the text '---PRODUCT-SEPARATOR---'.

        For EACH record from the all_product_markdowns, extract the following fields if available:
        url: Full URL that leads to the product page for a particular product(for example: a href="https://us.misumi-ec.com/vona2/mech/M0100000000/M0101000000/"),
        name: name of the product,
        description: description of product from class mc-text to the Read less text which is expanded through JS,
        image-link : from the src attribute of the product div
        alt-text : from the image tag of the product 

        Return ONLY a single valid JSON array of objects, like:
        [
        {{
            "url": "...",
            "name": "...",
            "desc": "...",
            "image-link": "...",
            "alt-text":"..."
        }},
        ...
        ]
        if a field is not found, set it to null.
        Do not include any explanation,markdown, or extra text.

        Raw Products Records
        {all_product_markdowns}
    """

    try:
        response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = prompt,
        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )
        )
        extracted_products = []
        try:
            extracted_products = json.loads(response.text)
        except Exception as parse_err:
                print("Parsing Error")
                with open(OUTPUT_FILE_NAME,'a',encoding = "utf-8") as f:
                    f.write(response.text.strip())
                
        with open(OUTPUT_FILE_NAME,'a',encoding="utf-8") as f:
                for product in extracted_products:
                    f.write(json.dumps(product,ensure_ascii=False) + "\n")
        print("Successfull")

    except Exception as e:
        print("No response from the API call to gemini")

llm_process()

