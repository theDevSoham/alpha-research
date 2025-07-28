# tests/integration/test_end_to_end.py
import time
import requests

BASE_URL = "http://localhost:8000"

def test_enrich_and_fetch_snippet():
    people = requests.get(f"{BASE_URL}/api/people").json()
    person = people[0]

    res = requests.post(f"{BASE_URL}/api/enrich/{person['id']}")
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    time.sleep(30)

    snippets = requests.get(f"{BASE_URL}/api/snippets/{person['company']['id']}").json()
    assert len(snippets) > 0
    assert "company_value_prop" in snippets[0]["payload"]
