import requests

API_KEY="4452b7105412acbd0f341fe6602dad80fcbf12f7c5bcede2b830c333eb3a9611"

def search_products(query):

    url="https://serpapi.com/search.json"

    params={
        "engine":"google_shopping",
        "q":query,
        "api_key":API_KEY,
        "location": "Mumbai, Maharashtra, India",
        "gl": "in",
        "hl": "en"
    }

    response=requests.get(url,params=params)

    return response.json()