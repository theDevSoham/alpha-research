from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alpha Research Platform")

app.include_router(api_router)
