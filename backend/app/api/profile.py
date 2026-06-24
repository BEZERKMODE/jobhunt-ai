import os
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing import List
from app import schemas, models
from app.api import deps
from sqlalchemy.orm import Session

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/me", response_model=schemas.UserOut)
async def read_profile(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    return current_user


@router.put("/me", response_model=schemas.UserOut)
async def update_profile(
    profile_data: schemas.ProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.auto_apply_enabled is not None:
        current_user.auto_apply_enabled = profile_data.auto_apply_enabled
    if profile_data.min_match_score is not None:
        current_user.min_match_score = profile_data.min_match_score
    if profile_data.preferred_locations is not None:
        current_user.preferred_locations = profile_data.preferred_locations
    if profile_data.preferred_roles is not None:
        current_user.preferred_roles = profile_data.preferred_roles

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/cv", response_model=schemas.CVOut)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    upload_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # We need to extract the text content
    from app.services.cv_parser import extract_text
    with open(upload_path, "rb") as buffer:
        text_content = extract_text(buffer.read(), file.filename)
        
    cv = models.CV(
        user_id=current_user.id, 
        filename=file.filename, 
        text_content=text_content
    )
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


@router.get("/cv", response_model=List[schemas.CVOut])
async def list_cvs(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    cvs = db.query(models.CV).filter(models.CV.user_id == current_user.id).all()
    return cvs
