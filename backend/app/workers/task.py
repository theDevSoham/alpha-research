from celery import shared_task
from app.db.database import SessionLocal
from app.db.models import Person, Company, ContextSnippet, SearchLog
from app.agent.research_agent import run_serp_agent
import uuid
from redis import Redis
import logging
import json

logger = logging.getLogger(__name__)

# Redis setup
r = Redis(host="redis", port=6379, decode_responses=True)

@shared_task(bind=True, name="app.workers.task.enrich_person_task")
def enrich_person_task(self, person_id: str):
    task_id = self.request.id  # Celery-generated job ID
    db = SessionLocal()
    try:
        r.set(f"job_progress:{task_id}", 10)

        # Fetch person
        person = db.query(Person).filter_by(id=person_id).first()
        if not person:
            r.set(f"job_progress:{task_id}", -1)
            return

        # Fetch associated company
        company = db.query(Company).filter_by(id=person.company_id).first()
        if not company:
            r.set(f"job_progress:{task_id}", -1)
            return

        # Run SERP agent to fetch enriched data
        result = run_serp_agent(person.full_name, person.email, company.domain)
        logger.info(f"[{task_id}] SERP Result: {json.dumps(result, indent=2)}")
        r.set(f"job_progress:{task_id}", 60)

        # Save context snippet
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
        r.set(f"job_progress:{task_id}", 80)

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
        r.set(f"job_progress:{task_id}", 100)

    except Exception as e:
        print(f"[ERROR] Task failed: {e}")
        r.set(f"job_progress:{task_id}", -1)
        db.rollback()
    finally:
        db.close()
