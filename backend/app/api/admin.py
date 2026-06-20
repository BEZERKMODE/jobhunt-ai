from fastapi import APIRouter, Depends, HTTPException, status
from app.core.config import settings
from app.dependencies.security import is_admin
from app.tasks.scraper import scrape_jobs_task

router = APIRouter()

@router.get("/scrape", tags=["admin"])
async def trigger_scrape(admin: None = Depends(is_admin)):
    """Trigger the job scraper as an admin.
    Returns a simple message indicating the scraper was started.
    """
    # Fire-and-forget Celery task
    scrape_jobs_task.delay()
    return {"status": "scrape started"}
