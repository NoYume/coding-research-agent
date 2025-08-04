import os
import json
import time
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)


    def search_companies(self, query: str, num_results: int = 5, max_retries: int = 2):
        for attempt in range(max_retries + 1):
            try:
                result = self.app.search(
                    query=f"{query} company pricing",
                    limit=num_results,
                    scrape_options=ScrapeOptions(
                        formats=["markdown"]
                    )
                )
                return result
            except Exception as e:
                error_msg = str(e).lower()
                
                if "502" in error_msg or "bad gateway" in error_msg:
                    if attempt < max_retries:
                        print(f"🔄 Firecrawl 502 error, retrying in {attempt + 1}s...")
                        time.sleep(attempt + 1)
                        continue
                    else:
                        print(f"❌ Firecrawl 502 error after {max_retries} retries: {e}")
                        return self._create_empty_result()
                
                if "json" in error_msg or "parse" in error_msg:
                    print(f"⚠️ Firecrawl response parsing error: {e}")
                    return self._create_empty_result()
                
                print(f"❌ Firecrawl search error: {e}")
                return self._create_empty_result()
            
        return self._create_empty_result()
        

    def scrape_company_page(self, url: str, max_retries: int = 2):
        for attempt in range(max_retries + 1):
            try:
                result = self.app.scrape_url(
                    url,
                    formats=["markdown"]
                )
                return result
            except Exception as e:
                error_msg = str(e).lower()
                
                if "502" in error_msg or "bad gateway" in error_msg:
                    if attempt < max_retries:
                        print(f"🔄 Scraping 502 error, retrying in {attempt + 1}s...")
                        time.sleep(attempt + 1)
                        continue
                    else:
                        print(f"⚠️ Scraping failed after {max_retries} retries: {url}")
                        return None
                    
                    print(f"⚠️ Scraping error for {url}: {e}")
                    return None
            
        return None
    
    
    def _create_empty_result(self):
        class EmptyResult:
            def __init__(self):
                self.data = []
        
        return EmptyResult()