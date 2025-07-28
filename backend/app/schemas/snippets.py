from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class PayloadSchema(BaseModel):
    company_value_prop: str
    product_names: List[str]
    pricing_model: str
    key_competitors: List[str]
    company_domain: str

class ContextSnippetOut(BaseModel):
    id: UUID
    entity_type: str
    entity_id: UUID
    snippet_type: str
    payload: PayloadSchema
    source_urls: List[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
