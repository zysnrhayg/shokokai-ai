# celery_app.py - Celery app and example task (generated)
# Use for async/long-running work: run worker with: celery -A celery_app worker -l info
# Move heavy operations from request handlers to .delay() calls; see DEPLOY.md.
from celery import Celery
import os

broker = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "app",
    broker=broker,
    backend=backend,
    include=[],
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(bind=True)
def example_task(self, x: int, y: int):
    """Example task: add two numbers. Call from Flask with: example_task.delay(1, 2)."""
    return x + y
