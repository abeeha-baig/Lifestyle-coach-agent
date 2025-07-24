import streamlit as st
from firecrawl import FirecrawlApp, ScrapeOptions

class FirecrawlService:
    def __init__(self):
        api_key = st.secrets["FIRECRAWL_API_KEY"]
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
            st.error(f"Search error: {e}")
            return []

    def scrape_article(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            st.error(f"Scraping error: {e}")
            return None
