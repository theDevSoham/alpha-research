from fastapi import APIRouter, HTTPException
from app.workers.task import enrich_person_task
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from app.db.database import SessionLocal
from app.db.models import Person, ContextSnippet
from app.schemas import PersonOut, ContextSnippetOut
from typing import List

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()

@router.post("/enrich/{person_id}")
def enrich_person(person_id: UUID):
    try:
        enrich_person_task.delay(str(person_id))
        return {"status": "enqueued", "person_id": str(person_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/people", response_model=List[PersonOut])
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).options(joinedload(Person.company)).all()

@router.get("/snippets/{company_id}", response_model=List[ContextSnippetOut])
def get_snippets_for_company(company_id: UUID, db: Session = Depends(get_db)):
    return db.query(ContextSnippet).filter_by(entity_type="company", entity_id=company_id).all()

@router.get("/healthz")
def health_check():
    return {"status": "ok"}
