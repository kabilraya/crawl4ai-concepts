from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import uuid
import asyncio
async def crawl_product_links_with_pagination():
    """
    Crawls only the first 4 pages 1,2,3,4
    """

    url = "https://hukut.com/mobile-phones"
    category_from_url = url.rstrip("/").split("/")[-1]
    all_product_links = []
    print(category_from_url)
    session_id = str(uuid.uuid4())

    browser_config = BrowserConfig(verbose = True, headless = True)
    async with AsyncWebCrawler(config = browser_config) as crawler:

        for page_num in range(1,5):

            print(f"Extracting the links in the {page_num} page")

            if(page_num == 1):
                results = await crawler.arun(url = url, config = CrawlerRunConfig(
                    delay_before_return_html=10.0,
                    mean_delay = 5.0,
                    css_selector="section div.group:has(a[href])",
                    cache_mode=CacheMode.DISABLED,
                    word_count_threshold = 10,
                    session_id = session_id,
                    scan_full_page= True,
                    simulate_user=True,
                    scroll_delay= 1.5,
                    remove_overlay_elements=True,
                    exclude_social_media_domains = [],
                    exclude_external_links=True,
                    exclude_social_media_links = True,
                    exclude_domains = [],
                )
                )
            else:
                """
                this part is for page not equal to 1 because it needs a js_code to click through the pages
                """
                js_to_click_next_page = f'document.querySelector("a[href=\'/{category_from_url}?page={page_num}\']").click()'
                results = await crawler.arun("https://hukut.com/mobile-phones",config = CrawlerRunConfig(
                    delay_before_return_html=10.0,
                    mean_delay = 5.0,
                    css_selector="section div.group:has(a[href])",
                    cache_mode=CacheMode.DISABLED,
                    word_count_threshold = 10,
                    session_id = session_id,
                    scan_full_page= True,
                    simulate_user=True,
                    js_code = js_to_click_next_page,
                    wait_for='css:section div.group:has(a[href])',
                    scroll_delay= 1.5,
                    remove_overlay_elements=True,
                    exclude_social_media_domains = [],
                    exclude_external_links=True,
                    exclude_social_media_links = True,
                    exclude_domains = [],
                    js_only=True
                    
                ))
            if results.success:
                new_links_found = 0
                for link in results.links["internal"]:
                    url = link.get("href")
                    if url not in all_product_links:
                        all_product_links.append(url)
                        new_links_found+=1
                        print(new_links_found)
            else:
                print(f"Crawling unsuccessful.")
                break;
    
    
        
    
    """
    Printing every internal links found in a file

    """

    file_name = "internal_links.txt"
    with open(file_name,"a" , encoding = "utf-8") as f:
        for idx, link in enumerate(all_product_links,start = 1):
            f.write(f"{idx} {link}"+ "\n")
    print(len(all_product_links))
    return all_product_links
