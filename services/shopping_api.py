import requests
from config import Config

def search_products(query):

    url = "https://serpapi.com/search.json"

    api_key = Config.SERPAPI_KEY
    if not api_key:
        print("Warning: SERPAPI_KEY is not set.")
        return {}

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key,
        "location": "Mumbai, Maharashtra, India",
        "gl": "in",
        "hl": "en"
    }

    response=requests.get(url,params=params)

    return response.json()