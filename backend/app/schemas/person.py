from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CompanyInfo(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True

class PersonOut(BaseModel):
    id: UUID
    full_name: str
    email: str
    title: str
    company: CompanyInfo
    created_at: datetime

    class Config:
        orm_mode = True
