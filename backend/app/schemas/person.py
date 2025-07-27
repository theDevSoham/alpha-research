from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PersonOut(BaseModel):
    id: UUID
    full_name: str
    email: str
    title: str
    company_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
