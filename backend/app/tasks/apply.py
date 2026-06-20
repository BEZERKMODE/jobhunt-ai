import asyncio
from app.worker import celery_app
from app.db.session import SessionLocal
from app.services.auto_apply import AutoApplyEngine
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.apply.process_application_task")
def process_application_task(application_id: str):
    """
    Celery task wrapper for the async AutoApplyEngine.
    """
    db = SessionLocal()
    try:
        engine = AutoApplyEngine(application_id=application_id, db_session=db)
        
        # Since celery runs synchronously by default, we run the async engine using asyncio
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(engine.run())
        
        if success:
            logger.info(f"Successfully processed application {application_id}")
        else:
            logger.warning(f"Application {application_id} processed but failed to complete all steps.")
            
    except Exception as e:
        logger.error(f"Error processing application {application_id}: {e}")
        db.rollback()
    finally:
        db.close()
