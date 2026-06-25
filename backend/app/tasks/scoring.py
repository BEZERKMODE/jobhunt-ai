from app.worker import celery_app
from app.db.session import SessionLocal
from app.models import CV, Job, JobMatchScore
from app.services.ai_scorer import evaluate_match, llm_score_resume_against_job
import asyncio
import json
from app.core.redis import redis_sync
from app.models import Application
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
        jobs = db.query(Job).limit(10).all()
        
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


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def score_job_against_cv(self, job_id: int, user_id: int):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        cv = db.query(CV).filter(CV.user_id == user_id).first()
        if not job or not cv:
            return

        result = asyncio.run(
            llm_score_resume_against_job(cv.text_content or "", job.description or "")
        )

        # Store enriched result on Application if exists
        apprec = db.query(Application).filter(
            Application.job_id == job_id, Application.user_id == user_id
        ).first()
        if apprec:
            apprec.match_score = result.get("match_score")
            apprec.ai_analysis = result
            apprec.cover_letter = result.get("cover_letter_draft")
            db.commit()

        # publish a task update to Redis so front-end can receive via WS
        try:
            payload = json.dumps({"type": "score_complete", "job_id": job_id, "score": result.get("match_score")})
            redis_sync.publish(f"task_updates:{user_id}", payload)
        except Exception:
            logger.exception("failed_to_publish_score_update")

    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc)
    finally:
        db.close()
