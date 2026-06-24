from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import JobListing
from app.models import CVFile
from app.models import Application

router = APIRouter()

@router.get("/stats", tags=["stats"])
def get_stats(db: Session = Depends(SessionLocal)):
    """Return simple aggregate statistics for the dashboard."""
    return {
        "total_jobs": db.query(JobListing).count(),
        "total_saved_cvs": db.query(CVFile).count(),
        "total_applications": db.query(Application).count(),
    }
