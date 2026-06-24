from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app import models
from app import schemas

router = APIRouter()

# ---- Static routes MUST come before dynamic /{job_id} routes ----

@router.post("/scrape")
async def scrape_jobs(
    query: str = "remote software engineer", 
    location: str = "remote",
    source: str = "indeed",
    limit: int = 5,
    current_user: models.User = Depends(deps.get_current_user), 
    db: Session = Depends(deps.get_db)
):
    from app.tasks.scrape_jobs import scrape_jobs_task
    scrape_jobs_task.delay(query=query, location=location, source=source, max_results=limit, user_id=current_user.id)
    return {"status": "Scraping task started"}


@router.post("/auto-apply")
async def auto_apply_all(
    current_user: models.User = Depends(deps.get_current_user), 
    db: Session = Depends(deps.get_db)
):
    from app.tasks.auto_apply import auto_apply_task
    # Find all pending applications for this user with score >= min_match_score
    apps = db.query(models.Application).filter(
        models.Application.user_id == current_user.id,
        models.Application.status == schemas.ApplicationStatus.pending,
        models.Application.match_score >= current_user.min_match_score
    ).all()
    
    for app in apps:
        auto_apply_task.delay(app.id)
        
    return {"status": f"Auto-apply process queued for {len(apps)} applications."}

# ---- Dynamic routes ----

@router.get("/", response_model=List[schemas.JobOut])
async def read_jobs(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(deps.get_db),
    current_user: deps.Optional[models.User] = Depends(deps.get_optional_user)
):
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
            
    return jobs

@router.get("/{job_id}", response_model=schemas.JobOut)
async def read_job(job_id: int, db: Session = Depends(deps.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/apply")
async def apply_job(job_id: int, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    application = db.query(models.Application).filter(
        models.Application.user_id == current_user.id,
        models.Application.job_id == job_id
    ).first()
    
    if not application:
        application = models.Application(user_id=current_user.id, job_id=job.id, status=schemas.ApplicationStatus.applied)
        db.add(application)
        db.commit()
    return {"status": "applied"}

