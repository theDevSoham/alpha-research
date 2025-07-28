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
        "company_value_prop": "AI-driven tools",
        "product_names": ["ToolX", "BotY"],
        "pricing_model": "Freemium",
        "key_competitors": ["CompetitorA", "CompetitorB"],
        "company_domain": "example.com"
    },
    "source_urls": ["https://example.com"],
    "created_at": str(datetime.now(timezone.utc))
}

broken_instance = deepcopy(full_instance)

def test_valid_payload_passes():
    validate(instance=full_instance, schema=ContextSnippetOut.model_json_schema())

def test_missing_required_field_fails():
    broken_instance["payload"] = broken_instance["payload"].copy()
    del broken_instance["payload"]["company_value_prop"]

    try:
        validate(instance=broken_instance, schema=ContextSnippetOut.model_json_schema())
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True
