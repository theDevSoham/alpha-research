from celery import Celery
import os

os.environ.setdefault("CELERY_BROKER_URL", os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"))

celery_app = Celery(
    "alpha_app",
    broker=os.environ["CELERY_BROKER_URL"],
)

celery_app.autodiscover_tasks(["app.workers"])
