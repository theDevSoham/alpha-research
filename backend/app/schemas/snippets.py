from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class PersonSchema(BaseModel):
    full_name: str
    profile_url: HttpUrl
    title: str
    current_company: str
    location: str
    summary: str
    social_presence: Optional[dict]  # or use a more structured schema if known


class SearchRankingSchema(BaseModel):
    top_result_position: int
    source: str
    search_query: str
    search_url: HttpUrl


class PublicWebPresenceSchema(BaseModel):
    official_website_found: bool
    search_rankings: dict  # or use Dict[str, SearchRankingSchema] for multiple engines


class CompanySchema(BaseModel):
    name: str
    role_of_person: str
    mentioned_by: str
    public_web_presence: PublicWebPresenceSchema
    product_description_available: bool
    description: str
    requires_further_research: bool


class MetaSchema(BaseModel):
    data_source: str
    query: str
    timestamp_utc: str
    total_results: int
    api_url: HttpUrl


class PayloadSchema(BaseModel):
    person: PersonSchema
    company: CompanySchema
    meta: MetaSchema


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
