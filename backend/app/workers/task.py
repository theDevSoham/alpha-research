from celery import shared_task
from app.db.database import SessionLocal
from app.db.models import Person, Company, ContextSnippet, SearchLog
from app.agent.research_agent import run_mock_agent
import uuid
import json

@shared_task(name="app.workers.task.enrich_person_task")
def enrich_person_task(person_id: str):
    db = SessionLocal()
    person = db.query(Person).filter_by(id=person_id).first()

    if not person:
        print(f"Person {person_id} not found.")
        db.close()
        return

    company = db.query(Company).filter_by(id=person.company_id).first()

    # Run mock agent (we’ll improve this later)
    result = run_mock_agent(person.full_name, person.email, company.domain)

    snippet_id = uuid.uuid4()
    db.add(ContextSnippet(
        id=snippet_id,
        entity_type="company",
        entity_id=company.id,
        payload=result["data"],
        source_urls=result["source_urls"],
        person_id=person.id,
    	company_id=company.id,
    ))

    # Save search logs
    for i, log in enumerate(result["logs"]):
        db.add(SearchLog(
            id=uuid.uuid4(),
            context_snippet_id=snippet_id,
            iteration=i + 1,
            query=log["query"],
            top_results=log["top_3"],
            person_id=person.id,
    		company_id=company.id,
        ))

    db.commit()
    db.close()
