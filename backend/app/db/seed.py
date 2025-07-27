import uuid
from sqlalchemy.orm import Session
from app.db.models import Campaign, Company, Person
from app.db.database import SessionLocal, engine, Base

def seed_data():
    db: Session = SessionLocal()

    # Avoid reseeding if people exist
    if db.query(Person).first():
        print("Seed already exists.")
        return

    campaign = Campaign(
        id=uuid.uuid4(),
        name="Sample Outreach Campaign"
    )
    db.add(campaign)

    company = Company(
        id=uuid.uuid4(),
        campaign_id=campaign.id,
        name="Acme Corp",
        domain="acme.com"
    )
    db.add(company)

    person1 = Person(
        id=uuid.uuid4(),
        company_id=company.id,
        full_name="Alice Johnson",
        email="alice@acme.com",
        title="CTO"
    )
    person2 = Person(
        id=uuid.uuid4(),
        company_id=company.id,
        full_name="Bob Smith",
        email="bob@acme.com",
        title="VP of Product"
    )

    db.add_all([person1, person2])
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()
