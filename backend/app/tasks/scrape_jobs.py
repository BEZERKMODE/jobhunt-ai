import asyncio
import json
import structlog
from app.worker import celery_app
from app.core.config import settings

log = structlog.get_logger()

DEFAULT_QUERIES = [
    ("software engineer", "remote"),
    ("python developer", "remote"),
    ("full stack developer", "remote"),
    ("backend engineer", "remote"),
]


@celery_app.task(bind=True, max_retries=2, default_retry_delay=30, name="app.tasks.scrape_jobs.scrape_jobs_task")
def scrape_jobs_task(self, query: str, location: str, source: str = "indeed", max_results: int = 20, user_id: int = None):
    """Scrape jobs and store them. Publishes progress via Redis pub/sub."""
    from app.db.session import SessionLocal
    from app.models import Job
    from app.services.scrapers.registry import get_scraper
    import redis

    db = SessionLocal()
    r = redis.from_url(settings.REDIS_URL)

    def publish(msg: dict):
        if user_id:
            r.publish(f"task_updates:{user_id}", json.dumps(msg))

    try:
        publish({"type": "scrape_started", "query": query, "task_id": self.request.id})

        scraper = get_scraper(source)
        jobs_data = asyncio.run(scraper.scrape(query, location, max_results))

        saved_count = 0
        for job_schema in jobs_data:
            existing = db.query(Job).filter(Job.external_id == job_schema.external_id).first()
            if existing:
                continue

            job = Job(**job_schema.model_dump())
            db.add(job)
            try:
                db.commit()
                db.refresh(job)
                saved_count += 1

                # Trigger scoring for all users with active CVs
                if user_id:
                    from app.tasks.score_jobs import score_job_for_user
                    score_job_for_user.delay(job.id, user_id)

            except Exception:
                db.rollback()
                continue

        publish({
            "type": "scrape_complete",
            "query": query,
            "new_jobs": saved_count,
            "total_found": len(jobs_data),
        })
        log.info("scrape_complete", query=query, saved=saved_count)
        return {"saved": saved_count, "found": len(jobs_data)}

    except Exception as exc:
        db.rollback()
        log.error("scrape_task_failed", error=str(exc))
        publish({"type": "scrape_error", "error": str(exc)})
        raise self.retry(exc=exc)
    finally:
        db.close()


@celery_app.task(name="app.tasks.scrape_jobs.scheduled_scrape")
def scheduled_scrape():
    """Periodic task — scrapes default queries for all users."""
    for query, location in DEFAULT_QUERIES:
        scrape_jobs_task.delay(query, location, "indeed", 15)
