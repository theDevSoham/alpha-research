import time
import random

def run_mock_agent(full_name, email, domain):
    query_base = f"{domain} company info"

    logs = []
    for i in range(3):
        time.sleep(3)  # ⏳ Add delay per iteration (3 * 3 = 9 seconds)
        logs.append({
            "query": f"{query_base} iteration {i+1}",
            "top_3": [
                {"url": f"https://example.com/article-{i}", "snippet": f"Info snippet {i}"}
                for i in range(3)
            ]
        })

    # Simulate a small final delay
    time.sleep(random.uniform(1.0, 2.5))  # total ~10–12 seconds

    return {
        "data": {
            "company_value_prop": "We automate boring tasks.",
            "product_names": ["BotSuite", "AutoMagic"],
            "pricing_model": "Subscription",
            "key_competitors": ["CompetitorX", "CompetitorY"],
            "company_domain": domain
        },
        "source_urls": [log["top_3"][0]["url"] for log in logs],
        "logs": logs
    }
