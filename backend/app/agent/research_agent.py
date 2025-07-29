# research_agent.py
import time
import os
from serpapi import GoogleSearch
from datetime import datetime, timezone

SERP_API_KEY = os.environ.get("SERP_API_KEY")

def run_serp_agent(full_name: str, email: str, domain: str):
    logs = []
    all_urls = set()
    linkedin_profile_url = ""
    person_location = ""
    person_title = ""
    company_description = ""
    company_mentioned_by = "N/A"
    search_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    serp_api_query_used = ""

    # Construct search queries
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

            serp_api_query_used = params["q"]
            top_results = []

            for result in results.get("organic_results", [])[:3]:
                url = result.get("link")
                snippet = result.get("snippet") or "No snippet"
                top_results.append({"url": url, "snippet": snippet})
                if url:
                    all_urls.add(url)

                if "linkedin.com/in" in url.lower():
                    linkedin_profile_url = url
                    person_title = next(
                        (ext for ext in result.get("rich_snippet", {}).get("top", {}).get("extensions", []) if "Product" in ext),
                        ""
                    )
                    person_location = next(
                        (ext for ext in result.get("rich_snippet", {}).get("top", {}).get("extensions", []) if "India" in ext),
                        ""
                    )
                    company_mentioned_by = result.get("source", "LinkedIn")

                if domain in snippet:
                    company_description = snippet

            logs.append({
                "query": query,
                "top_3": top_results
            })

        except Exception as e:
            logs.append({
                "query": query,
                "top_3": [{"url": "", "snippet": f"Error: {str(e)}"}]
            })

        time.sleep(2)

    payload = {
        "person": {
            "full_name": full_name,
            "profile_url": linkedin_profile_url or "N/A",
            "title": person_title or "N/A",
            "current_company": domain,
            "location": person_location or "N/A",
            "summary": f"{full_name} is currently associated with {domain}.",
            "social_presence": {
                "linkedin": linkedin_profile_url or "N/A"
            }
        },
        "company": {
            "name": domain,
            "role_of_person": person_title or "N/A",
            "mentioned_by": company_mentioned_by,
            "public_web_presence": {
                "official_website_found": False,
                "search_rankings": {
                    "google": {
                        "top_result_position": 1,
                        "source": company_mentioned_by,
                        "search_query": serp_api_query_used,
                        "search_url": f"https://www.google.com/search?q={serp_api_query_used.replace(' ', '+')}"
                    }
                }
            },
            "product_description_available": bool(company_description),
            "description": company_description or f"No public product description for {domain} found in search results.",
            "requires_further_research": not bool(company_description)
        },
        "meta": {
            "data_source": "SerpAPI",
            "query": serp_api_query_used,
            "timestamp_utc": search_timestamp,
            "total_results": 1,
            "api_url": "https://serpapi.com/search"  # Can be replaced with exact if available
        }
    }

    return {
        "data": payload,
        "source_urls": list(all_urls),
        "logs": logs
    }
