import logging
import asyncio
from app.worker import celery_app
from app.db.session import SessionLocal
from app.models import User, Job, JobMatchScore, Application
from app.schemas import ApplicationStatus
from app.services.auto_apply import AutoApplyEngine

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.auto_apply_tasks.process_auto_apply_queue")
def process_auto_apply_queue(user_id: str, dry_run: bool = True, threshold: int = 80):
    """
    Finds highly matched jobs for the user that they haven't applied to yet,
    creates Application records, and runs the AutoApplyEngine on them.
    """
    logger.info(f"Starting process_auto_apply_queue for user {user_id}")
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return "User not found"
            
        # Get top matches
        matches = db.query(JobMatchScore).filter(
            JobMatchScore.user_id == user_id,
            JobMatchScore.score >= threshold
        ).all()
        
        job_ids = [m.job_id for m in matches]
        
        # Filter jobs already applied to
        existing_apps = db.query(Application).filter(
            Application.user_id == user_id,
            Application.job_id.in_(job_ids)
        ).all()
        applied_job_ids = {app.job_id for app in existing_apps}
        
        jobs_to_apply = [jid for jid in job_ids if jid not in applied_job_ids]
        
        if not jobs_to_apply:
            logger.info("No new highly-matched jobs to apply to.")
            return "No new jobs to apply"
            
        # Limit to 5 for safety/prototype
        jobs_to_apply = jobs_to_apply[:5]
        
        applied_count = 0
        for jid in jobs_to_apply:
            # Create application record with status PENDING
            app_record = Application(user_id=user_id, job_id=jid, status=ApplicationStatus.PENDING)
            db.add(app_record)
            db.commit()
            
            engine = AutoApplyEngine(app_record.id, db)
            
            # Run asyncio code inside celery (synchronous context)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(engine.run(dry_run=dry_run))
            loop.close()
            
            if success:
                applied_count += 1
                
        return f"Auto-applied to {applied_count} jobs."
    except Exception as e:
        logger.error(f"Error in process_auto_apply_queue: {e}")
        db.rollback()
        return f"Failed: {e}"
    finally:
        db.close()
