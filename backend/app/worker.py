import os
from celery import Celery

# Use the REDIS_URL environment variable injected by Docker Compose.
# Fallback to the default service name if the variable is missing.
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery_app = Celery(
    'jobhunt',
    broker=redis_url,
    backend=redis_url,
)

@celery_app.task
def test_task():
    return 'Celery is working!'

