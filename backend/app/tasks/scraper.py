import httpx
from app.worker import celery_app
from app.db.session import SessionLocal
from app.models.job import JobListing
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.scraper.scrape_jobs_task")
def scrape_jobs_task(limit: int = 20):
    """
    Scraper task to fetch real remote software jobs from Remotive API.
    """
    logger.info(f"Starting scraping from Remotive API for up to {limit} jobs...")
    
    url = f"https://remotive.com/api/remote-jobs?category=software-dev&limit={limit}"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"Failed to fetch jobs from Remotive: {e}")
        return f"Failed: {e}"
        
    jobs_data = data.get("jobs", [])
    
    db = SessionLocal()
    saved_count = 0
    try:
        for item in jobs_data:
            # Check if url already exists
            existing = db.query(JobListing).filter(JobListing.url == item.get("url")).first()
            if not existing:
                # Truncate description if necessary or clean HTML
                import re
                clean_desc = re.sub(r'<[^>]+>', '', item.get("description", ""))
                
                job = JobListing(
                    title=item.get("title")[:200],
                    company=item.get("company_name")[:200],
                    location=item.get("candidate_required_location", "Remote"),
                    type=item.get("job_type", "Full-time"),
                    source="Remotive",
                    description=clean_desc[:1000] + ("..." if len(clean_desc) > 1000 else ""),
                    url=item.get("url"),
                    salary=None # Remotive sometimes returns salary as string, skipping for simplicity
                )
                db.add(job)
                saved_count += 1
                
        db.commit()
        logger.info(f"Successfully scraped and saved {saved_count} real jobs.")
    except Exception as e:
        logger.error(f"Error saving scraped jobs to DB: {e}")
        db.rollback()
    finally:
        db.close()
        
    return f"Scraped and saved {saved_count} jobs"

@celery_app.task(name="app.tasks.scraper.scrape_indeed_task")
def scrape_indeed_task(query: str = "remote software engineer", limit: int = 5):
    """
    Basic Playwright scraper for Indeed. Note: Indeed uses Cloudflare, so this may get blocked in production.
    """
    logger.info(f"Starting Indeed scraping for query: {query}")
    import asyncio
    from playwright.async_api import async_playwright
    import urllib.parse
    
    async def run_scraper():
        saved_count = 0
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                # Basic Indeed URL formatting
                url = f"https://www.indeed.com/jobs?q={urllib.parse.quote(query)}"
                logger.info(f"Navigating to {url}")
                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(3000) # Wait for potential Cloudflare challenge
                
                # Try to extract job cards
                job_cards = await page.locator("td.resultContent").all()
                logger.info(f"Found {len(job_cards)} job cards on Indeed.")
                
                db = SessionLocal()
                try:
                    for idx, card in enumerate(job_cards[:limit]):
                        title_loc = card.locator("h2.jobTitle span[title]")
                        company_loc = card.locator("span[data-testid='company-name']")
                        location_loc = card.locator("div[data-testid='text-location']")
                        
                        title = await title_loc.text_content() if await title_loc.count() > 0 else "Unknown Title"
                        company = await company_loc.text_content() if await company_loc.count() > 0 else "Unknown Company"
                        location = await location_loc.text_content() if await location_loc.count() > 0 else "Remote"
                        
                        # Generate a mock URL or try to find the href
                        link_loc = card.locator("a.jcs-JobTitle")
                        href = await link_loc.get_attribute("href") if await link_loc.count() > 0 else f"/viewjob?jk={idx}"
                        full_url = f"https://www.indeed.com{href}" if href.startswith("/") else href
                        
                        existing = db.query(JobListing).filter(JobListing.url == full_url).first()
                        if not existing:
                            job = JobListing(
                                title=title[:200],
                                company=company[:200],
                                location=location,
                                type="Full-time",
                                source="Indeed",
                                description=f"Job found via Indeed search: {query}",
                                url=full_url
                            )
                            db.add(job)
                            saved_count += 1
                    
                    db.commit()
                except Exception as e:
                    logger.error(f"Error saving Indeed jobs: {e}")
                    db.rollback()
                finally:
                    db.close()
                    
                await browser.close()
                return saved_count
        except Exception as e:
            logger.error(f"Playwright error during Indeed scrape: {e}")
            return 0

    loop = asyncio.get_event_loop()
    count = loop.run_until_complete(run_scraper())
    logger.info(f"Indeed scrape completed. Saved {count} jobs.")
    return f"Indeed Scraped and saved {count} jobs"
