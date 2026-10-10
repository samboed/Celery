from celery import Celery
from celery.result import AsyncResult

from src.config import CELERY_BROKER_URL, CELERY_BACKEND_URL


celery_app = Celery(
    "celery_app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
    include=['src.upscale.upscale']
)


def get_task(task_id: str):
    return AsyncResult(task_id, app=celery_app)
