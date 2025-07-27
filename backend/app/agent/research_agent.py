def run_mock_agent(full_name, email, domain):
    query_base = f"{domain} company info"

    logs = []
    for i in range(3):
        logs.append({
            "query": f"{query_base} iteration {i+1}",
            "top_3": [
                {"url": f"https://example.com/article-{i}", "snippet": f"Info snippet {i}"}
                for i in range(3)
            ]
        })

    # Simulated result
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
