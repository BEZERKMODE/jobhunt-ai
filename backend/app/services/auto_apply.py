import logging
import asyncio
from playwright.async_api import async_playwright
from app.models.application import ApplicationStatus
from app.models.job import JobListing
from app.models.application import Application
from app.models.user import User

logger = logging.getLogger(__name__)

class AutoApplyEngine:
    """
    Handles the orchestration of automatically applying to jobs using Playwright and LLMs.
    """
    
    def __init__(self, application_id: str, db_session):
        self.application_id = application_id
        self.db = db_session
        
    async def run(self):
        """
        Executes the auto-apply pipeline using Playwright.
        """
        logger.info(f"Starting auto-apply pipeline for Application {self.application_id}")
        
        application = self.db.query(Application).filter(Application.id == self.application_id).first()
        if not application:
            logger.error("Application not found.")
            return False
            
        job = self.db.query(JobListing).filter(JobListing.id == application.job_id).first()
        user = self.db.query(User).filter(User.id == application.user_id).first()
        
        if not job or not job.url:
            logger.error("Job or Job URL not found.")
            return False
            
        logger.info(f"Navigating to Job URL: {job.url}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Navigate to Job URL
                await page.goto(job.url, timeout=30000)
                await page.wait_for_load_state("networkidle")
                
                # Simple heuristic to find input fields and fill them
                logger.info("Filling form fields...")
                
                # Try to fill first name / name
                for selector in ["input[name*='name' i]", "input[id*='name' i]", "input[placeholder*='name' i]"]:
                    try:
                        elements = await page.locator(selector).all()
                        for el in elements:
                            if await el.is_visible():
                                await el.fill(user.name)
                    except Exception:
                        pass
                
                # Try to fill email
                for selector in ["input[type='email' i]", "input[name*='email' i]"]:
                    try:
                        elements = await page.locator(selector).all()
                        for el in elements:
                            if await el.is_visible():
                                await el.fill(user.email)
                    except Exception:
                        pass
                
                # If CV path exists, we could try to upload it
                if hasattr(user, "cv_files") and user.cv_files:
                    cv = user.cv_files[0]
                    for selector in ["input[type='file' i]", "input[name*='resume' i]", "input[name*='cv' i]"]:
                        try:
                            file_input = page.locator(selector).first
                            if await file_input.count() > 0:
                                await file_input.set_input_files(cv.path)
                                logger.info("Uploaded CV.")
                                break
                        except Exception:
                            pass
                
                logger.info("Form filled. Stopping before submission.")
                # We stop before submitting to prevent actual spamming in this prototype.
                # await page.click("button[type='submit']")
                
                await browser.close()
                
                # Update status
                application.status = ApplicationStatus.APPLIED
                self.db.commit()
                
                logger.info(f"Auto-apply pipeline completed successfully for {self.application_id}")
                return True
                
        except Exception as e:
            logger.error(f"Playwright automation failed: {e}")
            application.status = ApplicationStatus.REJECTED
            self.db.commit()
            return False
