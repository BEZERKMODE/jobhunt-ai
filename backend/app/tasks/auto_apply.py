import structlog
from datetime import datetime
from app.worker import celery_app

log = structlog.get_logger()


@celery_app.task(bind=True, max_retries=2, name="app.tasks.auto_apply.auto_apply_task")
def auto_apply_task(self, application_id: int):
    """
    Marks application as 'applied'. In production, this would drive
    a Playwright browser session to fill and submit the form.
    """
    from app.db.session import SessionLocal
    from app.models import Application, ApplicationStatus

    db = SessionLocal()
    try:
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            return {"error": "Application not found"}

        if app.status != ApplicationStatus.pending:
            return {"skipped": True, "reason": "Not in pending state"}

        user = app.user
        if not user.auto_apply_enabled:
            return {"skipped": True, "reason": "Auto-apply disabled for user"}

        if app.match_score and app.match_score < user.min_match_score:
            return {"skipped": True, "reason": f"Score {app.match_score} below threshold {user.min_match_score}"}

        # TODO: Playwright form filling here
        # For now, mark as applied with timestamp
        app.status = ApplicationStatus.applied
        app.applied_at = datetime.utcnow()
        db.commit()

        log.info("auto_apply_success", application_id=application_id, job_id=app.job_id)
        return {"success": True, "application_id": application_id}

    except Exception as exc:
        db.rollback()
        log.error("auto_apply_failed", application_id=application_id, error=str(exc))
        raise self.retry(exc=exc)
    finally:
        db.close()
