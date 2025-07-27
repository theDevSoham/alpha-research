from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import Campaign, Company, Person, ContextSnippet, SearchLog

router = APIRouter()

@router.post("/unseed")
def unseed_data():
    db = SessionLocal()

    # Delete in reverse dependency order
    db.query(Person).delete()
    db.query(Company).delete()
    db.query(Campaign).delete()
    db.commit()
    db.close()

    return {"message": "All seeded data has been deleted."}

@router.post("/unenrich")
def unenrich_data():
    db = SessionLocal()
    db.query(SearchLog).delete()
    db.query(ContextSnippet).delete()
    db.commit()
    db.close()

    return {"message": "All enrichment data has been deleted."}