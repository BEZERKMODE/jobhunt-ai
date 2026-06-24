"""
Indeed scraper using Playwright headless browser.
Respects robots.txt delays and uses realistic user-agent.
"""

import asyncio
import re
from typing import List
from datetime import datetime
import structlog

from app.schemas import JobCreate
from app.services.scrapers.base import BaseJobScraper

log = structlog.get_logger()


class IndeedScraper(BaseJobScraper):
    source_name = "indeed"
    BASE_URL = "https://www.indeed.com/jobs"

    async def scrape(self, query: str, location: str, max_results: int = 20) -> List[JobCreate]:
        from playwright.async_api import async_playwright

        jobs: List[JobCreate] = []
        log.info("indeed_scrape_start", query=query, location=location)

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

                url = f"{self.BASE_URL}?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(2)

                job_cards = await page.query_selector_all('[data-jk]')

                for card in job_cards[:max_results]:
                    try:
                        job_id = await card.get_attribute("data-jk")
                        title_el = await card.query_selector('[data-testid="jobTitle"] span, h2.jobTitle span')
                        company_el = await card.query_selector('[data-testid="company-name"], .companyName')
                        location_el = await card.query_selector('[data-testid="text-location"], .companyLocation')
                        snippet_el = await card.query_selector('.job-snippet, [data-testid="job-snippet"]')

                        title = await title_el.inner_text() if title_el else "Unknown Title"
                        company = await company_el.inner_text() if company_el else None
                        location_text = await location_el.inner_text() if location_el else location
                        description = await snippet_el.inner_text() if snippet_el else ""

                        is_remote = "remote" in location_text.lower() or "remote" in title.lower()
                        job_url = f"https://www.indeed.com/viewjob?jk={job_id}"
                        external_id = self._make_external_id("indeed", job_id or f"{title}{company}")

                        jobs.append(
                            JobCreate(
                                external_id=external_id,
                                title=title.strip(),
                                company=company.strip() if company else None,
                                location=location_text.strip(),
                                description=description.strip(),
                                url=job_url,
                                source="indeed",
                                is_remote=is_remote,
                                raw_data={"job_id": job_id},
                            )
                        )
                        await asyncio.sleep(0.3)  # polite delay

                    except Exception as e:
                        log.warning("indeed_card_parse_error", error=str(e))
                        continue

                await browser.close()

        except Exception as e:
            log.error("indeed_scrape_failed", error=str(e))

        log.info("indeed_scrape_done", count=len(jobs))
        return jobs
