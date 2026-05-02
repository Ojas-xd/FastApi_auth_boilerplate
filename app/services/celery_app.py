from celery import Celery
from app.core.security import settings
app=Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.services.mail"]
)
