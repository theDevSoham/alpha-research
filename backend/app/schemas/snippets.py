from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Any, List

class ContextSnippetOut(BaseModel):
    id: UUID
    entity_type: str
    entity_id: UUID
    snippet_type: str
    payload: Any
    source_urls: List[str]
    created_at: datetime

    class Config:
        orm_mode = True
