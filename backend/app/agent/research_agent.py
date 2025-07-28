# research_agent.py
import time
import os
from serpapi import GoogleSearch

SERP_API_KEY = os.environ.get("SERP_API_KEY")

def run_serp_agent(full_name, email, domain):
    logs = []
    all_urls = set()

    # Dynamic query patterns using full name, email, and domain
    queries = [
        f"{full_name} at {domain} overview",
        f"{full_name} email {email} company background",
        f"What does {domain} do {full_name}"
    ]

    for i, query in enumerate(queries):
        params = {
            "engine": "google",
            "q": query,
            "location": "",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "api_key": SERP_API_KEY,
            "num": 5
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            top_results = []
            for result in results.get("organic_results", [])[:3]:
                url = result.get("link")
                snippet = result.get("snippet") or "No snippet"
                top_results.append({"url": url, "snippet": snippet})
                if url:
                    all_urls.add(url)

            logs.append({
                "query": query,
                "top_3": top_results
            })

        except Exception as e:
            logs.append({
                "query": query,
                "top_3": [{"url": "", "snippet": f"Error: {str(e)}"}]
            })

        time.sleep(2)  # Delay to avoid rate limits

    synthesized_data = {
        "company_value_prop": "N/A",
        "product_names": [],
        "pricing_model": "N/A",
        "key_competitors": [],
        "company_domain": domain
    }

    return {
        "data": synthesized_data,
        "source_urls": list(all_urls),
        "logs": logs
    }
