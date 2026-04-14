import requests
from django.conf import settings
from django.core.cache import cache

class NewsService:
    @staticmethod
    def fetch_articles(query=None, country='us', category=None, source=None, sort_by='publishedAt', top_headlines=False):
        api_key = settings.NEWSDATA_API_KEY
        if not api_key:
            return {"status": "error", "message": "API key not found in settings."}

        # Create a unique cache key based on the parameters
        cache_key = f"newsdata_articles_{query}_{country}_{category}_{source}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # NewsData.io Latest News Endpoint
        url = "https://newsdata.io/api/1/latest"

        # Parameters Mapping for NewsData.io
        params = {
            "apikey": api_key,
            "size": 10,  # Max for Free Plan
            "language": "en"
        }

        if query:
            params["q"] = query
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        if source:
            params["domain"] = source

        try:
            # Increased timeout to 60 seconds to prevent Read timed out errors
            response = requests.get(url, params=params, timeout=60)
            
            # Handle specific status codes
            if response.status_code == 503:
                return {"status": "error", "message": "NewsData.io service is temporarily unavailable (503). Please try again in a few minutes."}
                
            response.raise_for_status()
            data = response.json()
            
            # Map NewsData.io response to match NewsAPI structure for compatibility with views/templates
            if data.get('status') == 'success':
                mapped_articles = []
                for item in data.get('results', []):
                    mapped_articles.append({
                        'title': item.get('title'),
                        'description': item.get('description') or item.get('content'),
                        'url': item.get('link'),
                        'urlToImage': item.get('image_url'),
                        'publishedAt': item.get('pubDate'),
                        'source': {
                            'id': item.get('source_id'),
                            'name': item.get('source_name') or item.get('source_id')
                        }
                    })
                
                result = {
                    "status": "ok", # Mimic NewsAPI success status
                    "articles": mapped_articles,
                    "totalResults": data.get('totalResults', 0)
                }
                
                # Cache article results for 10 minutes (600 seconds)
                cache.set(cache_key, result, 600)
                return result
            else:
                return {"status": "error", "message": data.get('message', 'API returned an error')}
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                return {"status": "error", "message": "NewsData.io service is temporarily unavailable. The server is likely overloaded."}
            return {"status": "error", "message": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"status": "error", "message": f"An error occurred: {err}"}


    @staticmethod
    def get_sources(country=None, category=None, language='en'):
        api_key = settings.NEWSDATA_API_KEY
        if not api_key:
            return []
        
        # Create a unique cache key based on the parameters
        cache_key = f"newsdata_sources_{country}_{category}_{language}"
        cached_sources = cache.get(cache_key)
        if cached_sources:
            return cached_sources
        
        # NewsData.io Sources Endpoint
        url = "https://newsdata.io/api/1/sources"
        params = {
            "apikey": api_key,
            "language": language
        }
        
        if country:
            params["country"] = country
        if category:
            params["category"] = category
            
        try:
            # Increased timeout to 60 seconds to prevent Read timed out errors
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'success':
                sources = []
                for item in data.get('results', []):
                    sources.append({
                        'id': item.get('id'),
                        'name': item.get('name') or item.get('id')
                    })
                
                # Cache the results for 2 hours (7200 seconds)
                cache.set(cache_key, sources, 7200)
                return sources
        except Exception:
            return []
        return []
