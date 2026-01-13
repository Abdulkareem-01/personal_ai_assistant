"""from duckduckgo_search import DDGS

def web_search(query, max_results=5):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title"),
                "body": r.get("body"),
                "link": r.get("href")
            })

    return results"""
    
from ddgs import DDGS

def web_search(query, max_results=6):
    documents = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            body = r.get("body")
            if body and len(body.split()) > 40:
                documents.append(body)

    return documents
