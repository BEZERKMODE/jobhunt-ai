import os
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing import List
from app import schemas, models
from app.api import deps
from sqlalchemy.orm import Session

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/me", response_model=schemas.profile.ProfileRead)
async def read_profile(
    current_user: models.user.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    # ProfileRead maps directly to the User model fields (name, email, role, plan, created_at)
    return current_user


@router.put("/me", response_model=schemas.profile.ProfileRead)
async def update_profile(
    profile_data: schemas.profile.ProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_user),
):
    if profile_data.name is not None:
        current_user.name = profile_data.name
    if profile_data.email is not None:
        current_user.email = profile_data.email
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/cv", response_model=schemas.cv.CVRead)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_user),
):
    upload_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())
    cv = models.cv.CVFile(user_id=current_user.id, filename=file.filename, file_url=upload_path)
    db.add(cv)
    db.commit()
    db.refresh(cv)

    # Trigger background scoring task
    try:
        from app.tasks.scoring import score_cv_against_jobs_task
        score_cv_against_jobs_task.delay(str(cv.id), str(current_user.id))
    except Exception:
        pass  # Don't fail the upload if scoring task fails to queue

    return cv


@router.get("/cv", response_model=List[schemas.cv.CVRead])
async def list_cvs(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_user),
):
    cvs = db.query(models.cv.CVFile).filter(models.cv.CVFile.user_id == current_user.id).all()
    return cvs
