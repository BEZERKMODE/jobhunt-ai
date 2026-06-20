from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app import models
from app import schemas

router = APIRouter()

# ---- Static routes MUST come before dynamic /{job_id} routes ----

@router.post("/scrape/indeed")
async def scrape_indeed(
    query: str = "remote software engineer", 
    limit: int = 5,
    current_user: models.User = Depends(deps.get_current_user), 
    db: Session = Depends(deps.get_db)
):
    from app.tasks.scraper import scrape_indeed_task
    scrape_indeed_task.delay(query=query, limit=limit)
    return {"status": "Scraping task started"}

@router.post("/auto-apply")
async def auto_apply_all(
    current_user: models.User = Depends(deps.get_current_user), 
    db: Session = Depends(deps.get_db)
):
    return {"status": "Auto-apply process started for your top matches"}

# ---- Dynamic routes ----

@router.get("/", response_model=List[schemas.JobRead])
async def read_jobs(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(deps.get_db),
    current_user: deps.Optional[models.User] = Depends(deps.get_optional_user)
):
    jobs = db.query(models.JobListing).offset(skip).limit(limit).all()
    
    if current_user:
        scores = db.query(models.JobMatchScore).filter(
            models.JobMatchScore.user_id == current_user.id
        ).all()
        score_map = {str(score.job_id): score.score for score in scores}
        for job in jobs:
            job.match_score = score_map.get(str(job.id))
            
    return jobs

@router.get("/{job_id}", response_model=schemas.JobRead)
async def read_job(job_id: str, db: Session = Depends(deps.get_db)):
    job = db.query(models.JobListing).filter(models.JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/{job_id}/save")
async def save_job(job_id: str, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    job = db.query(models.JobListing).filter(models.JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    saved = db.query(models.SavedJob).filter(
        models.SavedJob.user_id == current_user.id,
        models.SavedJob.job_id == job_id
    ).first()
    
    if not saved:
        saved = models.SavedJob(user_id=current_user.id, job_id=job.id)
        db.add(saved)
        db.commit()
    return {"status": "saved"}

@router.delete("/{job_id}/save")
async def unsave_job(job_id: str, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    saved = db.query(models.SavedJob).filter(
        models.SavedJob.user_id == current_user.id,
        models.SavedJob.job_id == job_id
    ).first()
    
    if saved:
        db.delete(saved)
        db.commit()
    return {"status": "unsaved"}

@router.post("/{job_id}/apply")
async def apply_job(job_id: str, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    job = db.query(models.JobListing).filter(models.JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    application = db.query(models.Application).filter(
        models.Application.user_id == current_user.id,
        models.Application.job_id == job_id
    ).first()
    
    if not application:
        application = models.Application(user_id=current_user.id, job_id=job.id, status=schemas.ApplicationStatus.APPLIED)
        db.add(application)
        db.commit()
    return {"status": "applied"}
