from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app import models
from app import schemas
from app.core import security

router = APIRouter()

@router.get("/", response_model=List[schemas.ApplicationOut])
async def read_applications(skip: int = 0, limit: int = 100, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    apps = db.query(models.Application).filter(models.Application.user_id == current_user.id).offset(skip).limit(limit).all()
    return apps

@router.post("/", response_model=schemas.ApplicationOut)
async def create_application(application: schemas.ApplicationCreate, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    db_app = models.Application(
        job_id=application.job_id,
        user_id=current_user.id,
        status=schemas.ApplicationStatus.PENDING
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app
