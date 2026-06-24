from app.worker import celery_app
from app.db.session import SessionLocal
from app.models import CVFile
from app.models import JobListing
from app.models import JobMatchScore
from app.services.ai_scorer import evaluate_match
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.scoring.score_cv_against_jobs_task")
def score_cv_against_jobs_task(cv_id: str, user_id: str):
    """
    Background task to parse a CV and score it against available jobs.
    """
    db = SessionLocal()
    try:
        cv = db.query(CV).filter(CV.id == cv_id).first()
        if not cv:
            logger.error(f"CV {cv_id} not found.")
            return
            
        # In a real app, parse PDF text from cv.filepath here using PyPDF2
        # For this prototype, we'll use a mocked text or basic parsing if text is stored
        # Parse PDF using PyPDF2
        try:
            from PyPDF2 import PdfReader
            pdf_path = cv.file_url  # Assume this is a filesystem path
            reader = PdfReader(pdf_path)
            text_parts = []
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            cv_text = "\n".join(text_parts)
        except Exception as e:
            logger.error(f"Failed to parse CV PDF {cv.id}: {e}")
            cv_text = ""

        
        # Get jobs to score against (e.g. all jobs, or active jobs)
        jobs = db.query(JobListing).limit(10).all()
        
        for job in jobs:
            result = evaluate_match(cv_text, job.description)
            
            score_record = JobMatchScore(
                user_id=user_id,
                job_id=job.id,
                score=result.get("score", 0.0),
                verdict=result.get("verdict", ""),
                missing_skills=result.get("missing_skills", [])
            )
            db.add(score_record)
            
        db.commit()
        logger.info(f"Successfully scored CV {cv_id} against {len(jobs)} jobs.")
    except Exception as e:
        logger.error(f"Error scoring CV {cv_id}: {e}")
        db.rollback()
    finally:
        db.close()
