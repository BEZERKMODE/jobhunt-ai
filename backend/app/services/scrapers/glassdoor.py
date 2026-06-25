"""
Glassdoor Jobs Scraper using Playwright.
Glassdoor requires scrolling and has dynamic content loading.
"""

import asyncio
import random
import re
from typing import List
import structlog

from app.schemas import JobCreate
from app.services.scrapers.base import BaseJobScraper

log = structlog.get_logger()


class GlassdoorScraper(BaseJobScraper):
    source_name = "glassdoor"
    BASE_URL = "https://www.glassdoor.com/Job/jobs.htm"

    async def scrape(
        self, query: str, location: str, max_results: int = 20
    ) -> List[JobCreate]:
        """Scrape Glassdoor job listings."""
        from playwright.async_api import async_playwright

        jobs: List[JobCreate] = []
        log.info("glassdoor_scrape_start", query=query, location=location)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-setuid-sandbox"],
                )

                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                )

                page = await context.new_page()

                # Build Glassdoor search URL
                url = (
                    f"{self.BASE_URL}?"
                    f"keyword={query.replace(' ', '+')}&"
                    f"location={location.replace(' ', '+')}"
                )

                log.debug("glassdoor_url", url=url)

                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(2, 4))

                # Scroll to load more jobs dynamically
                for _ in range(2):
                    await page.evaluate("window.scrollBy(0, window.innerHeight)")
                    await asyncio.sleep(random.uniform(1, 2))

                # Extract job listings
                job_cards = await page.query_selector_all("li[data-job-id]")
                log.debug("glassdoor_found_cards", count=len(job_cards))

                for card in job_cards[:max_results]:
                    try:
                        job_id = await card.get_attribute("data-job-id")

                        title_el = await card.query_selector(".jobTitle")
                        company_el = await card.query_selector(".companyName")
                        location_el = await card.query_selector(".location")
                        salary_el = await card.query_selector(".salary")

                        title = await title_el.inner_text() if title_el else "Unknown"
                        company = await company_el.inner_text() if company_el else "Unknown"
                        location_text = (
                            await location_el.inner_text()
                            if location_el
                            else location
                        )
                        salary_text = await salary_el.inner_text() if salary_el else None

                        # Parse salary range
                        salary_min, salary_max = None, None
                        if salary_text and "$" in salary_text:
                            # Extract: "$60K - $80K" → (60000, 80000)
                            matches = re.findall(r"\$(\d+)K?", salary_text)
                            if len(matches) >= 2:
                                salary_min = int(matches[0]) * 1000
                                salary_max = int(matches[1]) * 1000

                        is_remote = "remote" in location_text.lower()
                        job_url = f"https://www.glassdoor.com/job-listing/{job_id}"
                        external_id = self._make_external_id("glassdoor", job_id or title)

                        jobs.append(
                            JobCreate(
                                external_id=external_id,
                                title=title.strip(),
                                company=company.strip(),
                                location=location_text.strip(),
                                url=job_url,
                                source="glassdoor",
                                is_remote=is_remote,
                                salary_min=salary_min,
                                salary_max=salary_max,
                                raw_data={"job_id": job_id},
                            )
                        )

                        log.debug(
                            "glassdoor_job_parsed",
                            title=title,
                            company=company,
                        )

                    except Exception as e:
                        log.warning("glassdoor_card_parse_error", error=str(e))
                        continue

                await browser.close()

        except Exception as e:
            log.error("glassdoor_scrape_failed", error=str(e))

        log.info("glassdoor_scrape_done", count=len(jobs))
        return jobs
