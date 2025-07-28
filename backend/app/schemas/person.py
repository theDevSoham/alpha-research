from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CompanyInfo(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }

class PersonOut(BaseModel):
    id: UUID
    full_name: str
    email: str
    title: str
    company: CompanyInfo
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
