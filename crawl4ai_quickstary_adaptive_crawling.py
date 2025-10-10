import asyncio
from crawl4ai import AsyncWebCrawler,AdaptiveCrawler

async def adaptive_crawler():
    async with AsyncWebCrawler() as crawler:
        #make the object of Adaptive web crawler
        adaptive_crawler = AdaptiveCrawler(crawler)

        result = await adaptive_crawler.digest(start_url = "https://docs.python.org/3/",query="async context managers")
        
        """
        async def digest(
            start_url: str,
            query: str,
            resume_from: str | None = None
            ) -> CoroutineType[Any, Any, CrawlState]:
    
            Crawl and extract structured information from the given URL adaptively.

            Args:
            start_url (str): 
            The starting point of the crawl process. 
            Must be a valid URL from which the crawler begins extraction.

            query (str): 
            The information extraction or search query guiding the crawler.
            This determines what type of content or data to extract from the site.

            resume_from (str | None, optional): 
            A checkpoint or saved crawl state to resume from.
            If None, the crawl starts fresh from the given start_url.

        Returns:
            CoroutineType[Any, Any, CrawlState]: 
            An awaitable coroutine that, when awaited, returns a CrawlState object 
            containing details about the crawl session, including results, 
            visited URLs, and crawl progress.

        Example:
        >>> crawler = AdaptiveCrawler()
        >>> state = await crawler.digest(
        ...     start_url="https://example.com/products",
        ...     query="Find all laptop listings",
        ... )
        >>> print(state.results)
        """
    
        adaptive_crawler.print_stats()
        print(f"Crawled {len(result.crawled_urls)} pages")
        print(f"Achieved {adaptive_crawler.confidence:.0%} confidence")
        relevant_content = adaptive_crawler.get_relevant_content(top_k=5)
        print(relevant_content)
        for page in relevant_content:
            print(page["content"],"\n")
            

asyncio.run(adaptive_crawler())
