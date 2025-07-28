from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.dev_tools import router as dev_router
from app.api.ws import router as websocket_router
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alpha Research Platform")

app.include_router(api_router, prefix="/api")
app.include_router(dev_router, prefix="/dev", tags=["Dev Tools"])
app.include_router(websocket_router, tags=["Websockets"])
