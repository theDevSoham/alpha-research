from fastapi import APIRouter
from celery_worker import celery_app
from celery.result import AsyncResult
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
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
def enrich_person(person_id: str):
    task = celery_app.send_task(
        "app.workers.task.enrich_person_task",
        args=[person_id]
    )
    return {"status": "enrichment queued", "task_id": task.id}

@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
    
@router.get("/people", response_model=List[PersonOut])
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).options(joinedload(Person.company)).all()

@router.get("/snippets/{company_id}", response_model=List[ContextSnippetOut])
def get_snippets_for_company(company_id: UUID, db: Session = Depends(get_db)):
    return (
        db.query(ContextSnippet)
        .filter_by(entity_type="company", entity_id=company_id)
        .order_by(desc(ContextSnippet.created_at))
        .all()
    )

@router.get("/healthz")
def health_check():
    return {"status": "ok"}
