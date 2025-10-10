import asyncio
from crawl4ai import AsyncWebCrawler,CacheMode,BrowserConfig,CrawlerRunConfig,DefaultMarkdownGenerator,BFSDeepCrawlStrategy,CrawlResult
import re
from bs4 import BeautifulSoup
import re
async def simple_crawling_examples_with_configs():
    browser_conf = BrowserConfig(headless = True, verbose = True,java_script_enabled = True)

    run_conf = CrawlerRunConfig(
        # ==============================================================================
        #                      CRAWL CONTENT EXTRACTION & CLEANING
        # ==============================================================================
        word_count_threshold = 50,                 # Minimum word count for a content block to be considered valid/not noise.
        # extraction_strategy = None,                # Specifies a strategy (e.g., LLM, Regex) for structured data extraction. None uses default text/markdown.
        # chunking_strategy = None,                  # Strategy (e.g., Regex, SlidingWindow) for breaking content into small pieces (chunks) for RAG/LLMs.
        markdown_generator = DefaultMarkdownGenerator(), # Engine to convert cleaned HTML content into Markdown markup.
        only_text = False,                         # If True, strips all formatting. False retains structure for Markdown.
        # css_selector = ".Ms6aG",                       # A CSS selector to target a specific section of the page (e.g., '#main-content').
        # target_elements = ['div'],     # Prioritized HTML tags/selectors to search for primary content.
        excluded_tags = ['header', 'nav', 'footer', 'aside', 'form', 'script', 'style'], # Tags to remove from the content before processing.
        remove_forms = True,                       # If True, eliminates all <form> elements and their content.
        parser_type = "lxml",                      # The HTML parser library to use ('lxml' is typically fastest).

        # ==============================================================================
        #                      NETWORK, PROXY, AND CACHING
        # ==============================================================================
        # proxy_config = None,                       # Configuration for a proxy server (IP/Port/Credentials).
        # proxy_rotation_strategy = None,            # Strategy for rotating through multiple proxies if provided.
        disable_cache = False,                     # Completely disables the cache mechanism for this run.
        no_cache_read = False,                     # Prevents reading from the cache for a result.
        no_cache_write = False,                    # Prevents writing a successful result to the cache.
        method = "GET",                            # The HTTP method to use for the request.
        check_robots_txt = False,                  # If True, respects the website's robots.txt file.
        # user_agent_mode="rotate",                  # Rotate user agents
        # user_agent_generator_config={
        #     "device_types": ["desktop", "mobile"], # Mimic real browsers
        #     "browsers": ["chrome", "firefox", "edge"],
        # },

        # ==============================================================================
        #                     BROWSER TIMING & DYNAMIC RENDERING
        # ==============================================================================
        # page_timeout = 30,                        # Maximum time (in seconds) to wait for the page to load.
        delay_before_return_html = 5.0,            # Time (in seconds) to wait *after* the page is considered loaded and JS is executed.
        mean_delay = 2.0,                          # Average random delay (in seconds) between requests to simulate human behavior.
        max_range = 6.0,                           # The maximum variation (randomness) for the delay calculation.
        semaphore_count = 5,                       # Limits the number of concurrent URLs scraped at once.
        js_code = """
            // Scroll to bottom to trigger lazy loading
            window.scrollTo(0, document.body.scrollHeight); 
            return true;
        """,
        scan_full_page = True,                    # If True, ensures the browser has rendered the full document height.
        scroll_delay = 1.5,                        # Time (in seconds) to wait between individual scroll steps.
        max_scroll_steps = 10,                   # Limits the number of times the page will automatically scroll down.
        process_iframes = False,                   # If True, content will be extracted from embedded IFRAMEs.
        remove_overlay_elements = True,           # Attempts to hide or remove sticky headers, consent popups, etc.
        simulate_user = True,                     # Enables aggressive user behavior simulation (e.g., random mouse movements).
        override_navigator = True,                # Enables techniques to spoof browser properties to prevent bot detection.
        magic = True,                             # Placeholder for aggressive, pre-configured stealth/anti-detection settings.
        adjust_viewport_to_content = True,        # Automatically adjusts the browser viewport size to match content dimensions.

        # ==============================================================================
        #                      LINK FILTERING & CRAWLING
        # ==============================================================================
        exclude_social_media_domains = [],         # List of social media domains to ignore (e.g., 'facebook.com').
        exclude_external_links = True,            # If True, filters out links pointing to other domains.
        exclude_social_media_links = True,        # If True, filters out links pointing to social media domains.
        exclude_domains = [],                      # List of domains to exclude from the crawl.
        # deep_crawl_strategy = BFSDeepCrawlStrategy(
        #     max_pages=300,
        #     max_depth=2,
        #     include_external=False,
        #     # filter_chain=FilterChain([url_filter])
        # ),  
        # url_matcher = r"daraz\.com\.np/catalog",                        # Custom object to filter URLs based on a pattern/logic.

        # ==============================================================================
        #                     DEBUGGING & EXPERIMENTAL
        # ==============================================================================
        verbose = True,                            # Enables detailed logging output to the console.
        log_console = False,                       # If True, logs JavaScript console messages from the browser.
        capture_network_requests = False,          # If True, logs all network requests made by the browser.
        capture_console_messages = False,          # Alias for log_console.
        experimental = {},                         # Dictionary for passing experimental or undocumented parameters.
    )

    #crawling a single page of Daraz and storing the url and content in separate file

    async with AsyncWebCrawler(config = browser_conf) as crawler:
        result = await crawler.arun("https://www.daraz.com.np/",config = run_conf) #this returns the list of pages that is crawled
        #for simple crawling list with only one pageresult

        if result.success:
            print("Successfully crawled the given website")

            print("Content",result.markdown[:500])

            for image in result.media["images"]:
                print(f"Found Image: {image['src']}")
            for link in result.links['internal']:
                print(f"Internal Links: {link['href']}")

        else:
            print("Crawling Unsuccessfully")        

        

asyncio.run(simple_crawling_examples_with_configs())