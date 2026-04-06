from django.shortcuts import render
from .services import NewsService
from datetime import datetime

def index(request):
    query = request.GET.get('q', '')
    source = request.GET.get('source', '')
    country = request.GET.get('country', 'us')  # Default to 'us'
    sort_by = request.GET.get('sort_by', 'relevancy')
    top_headlines = request.GET.get('type', 'everything') == 'top-headlines'
    
    # Only fetch if there's a reason to (query, specifically headlines, or source selected)
    # If top_headlines is selected, we usually fetch by country even without a query
    is_initial = not (query or source or (top_headlines and country))
    
    articles = []
    error_message = None
    
    if not is_initial:
        # Fetch news articles
        news_data = NewsService.fetch_articles(
            query=query if query else None,
            source=source if source else None,
            country=country,
            sort_by=sort_by,
            top_headlines=top_headlines
        )
        
        if news_data.get('status') == 'ok':
            articles = news_data.get('articles', [])
            # Simple summary truncation and date formatting
            for idx, article in enumerate(articles):
                if article.get('description'):
                    article['summary'] = article['description'][:150] + "..." if len(article['description']) > 150 else article['description']
                else:
                    article['summary'] = "No description available."
                
                # Format date
                pub_date = article.get('publishedAt')
                if pub_date:
                    try:
                        dt = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ")
                        article['formatted_date'] = dt.strftime("%b %d, %Y")
                    except ValueError:
                        article['formatted_date'] = pub_date[:10]
                else:
                    article['formatted_date'] = "Unknown Date"
        else:
            error_message = news_data.get('message', 'Failed to fetch news.')

    # Fetch sources to populate dropdown
    sources = NewsService.get_sources()
    
    context = {
        'articles': articles,
        'query': query,
        'source': source,
        'sort_by': sort_by,
        'top_headlines': top_headlines,
        'sources': sources,
        'error_message': error_message
    }
    
    return render(request, 'newsapp/index.html', context)
