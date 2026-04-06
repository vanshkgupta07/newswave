import requests
from django.conf import settings

class NewsService:
    @staticmethod
    def fetch_articles(query=None, country='us', category=None, source=None, sort_by='publishedAt', top_headlines=False):
        api_key = settings.NEWSAPI_KEY
        if not api_key:
            return {"status": "error", "message": "API key not found in settings."}

        base_url = "https://newsapi.org/v2/"
        endpoint = "top-headlines" if top_headlines else "everything"
        url = f"{base_url}{endpoint}"

        params = {
            "apiKey": api_key,
            "pageSize": 20,
            "language": "en"
        }

        if top_headlines:
            if country and not source:
                params["country"] = country
            if category:
                params["category"] = category
            if source:
                params["sources"] = source
            if query:
                params["q"] = query
        else:
            if query:
                # Use qInTitle for much higher relevance (avoids 'trash' that just mentions the word)
                params["qInTitle"] = query
            else:
                # If no query is provided, we won't set a default, allowing the view to handle the empty state.
                pass 
            
            if source:
                params["sources"] = source
            if sort_by:
                params["sortBy"] = sort_by

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {"status": "error", "message": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"status": "error", "message": f"An error occurred: {err}"}

    @staticmethod
    def get_sources():
        # Fetching sources to populate the filter dropdown
        api_key = settings.NEWSAPI_KEY
        url = "https://newsapi.org/v2/top-headlines/sources"
        params = {"apiKey": api_key, "language": "en"}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('sources', [])
        except Exception:
            return []
