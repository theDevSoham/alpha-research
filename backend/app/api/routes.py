from fastapi import APIRouter, HTTPException
from app.workers.task import enrich_person_task
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Person
from app.schemas.person import PersonOut
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
    return db.query(Person).all()


@router.get("/healthz")
def health_check():
    return {"status": "ok"}
