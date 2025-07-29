from uuid import uuid4
from datetime import datetime, timezone
from jsonschema import validate, ValidationError
from app.schemas import ContextSnippetOut
from copy import deepcopy

full_instance = {
    "id": str(uuid4()),
    "entity_type": "company",
    "entity_id": str(uuid4()),
    "snippet_type": "research",
    "payload": {
        "company": {
            "name": "Example Inc.",
            "domain": "example.com",
            "value_prop": "AI-driven analytics",
            "product_names": ["ToolX", "InsightY"],
            "pricing_model": "Freemium",
            "key_competitors": ["CompetitorA", "CompetitorB"]
        },
        "person": {
            "full_name": "Jane Doe",
            "role": "Chief Data Officer",
            "notable_mentions": [
                "Spoke at AI Summit 2023",
                "Published a paper on federated learning"
            ],
            "reputation_summary": "Recognized for leading data ethics initiatives."
        }
    },
    "source_urls": ["https://example.com"],
    "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
}

broken_instance = deepcopy(full_instance)

def test_valid_payload_passes():
    validate(instance=full_instance, schema=ContextSnippetOut.model_json_schema())

def test_missing_required_field_fails():
    broken_instance["payload"]["company"].pop("value_prop", None)

    try:
        validate(instance=broken_instance, schema=ContextSnippetOut.model_json_schema())
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True

def test_missing_person_section_fails():
    broken_payload = deepcopy(full_instance["payload"])
    broken_payload.pop("person", None)

    instance = deepcopy(full_instance)
    instance["payload"] = broken_payload

    try:
        validate(instance=instance, schema=ContextSnippetOut.model_json_schema())
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True

