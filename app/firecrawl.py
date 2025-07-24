import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is not set.")
        self.app = FirecrawlApp(api_key=api_key)

    def search_articles(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query=f"{query} wellness blog site:medium.com OR site:healthline.com OR site:mindbodygreen.com",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(e)
            return []

    def scrape_article(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(e)
            return None
