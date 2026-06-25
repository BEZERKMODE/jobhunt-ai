"""
Stack Overflow Jobs Scraper - Developer-focused jobs.
Targets Stack Overflow's job board with developer positions.
"""

import asyncio
import random
from typing import List
import structlog

from app.schemas import JobCreate
from app.services.scrapers.base import BaseJobScraper

log = structlog.get_logger()


class StackOverflowScraper(BaseJobScraper):
    source_name = "stackoverflow"
    BASE_URL = "https://stackoverflow.com/jobs"

    async def scrape(
        self, query: str, location: str, max_results: int = 20
    ) -> List[JobCreate]:
        """Scrape Stack Overflow job listings."""
        from playwright.async_api import async_playwright

        jobs: List[JobCreate] = []
        log.info("stackoverflow_scrape_start", query=query, location=location)

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

                # Build Stack Overflow search URL
                url = f"{self.BASE_URL}?q={query}&l={location}"

                log.debug("stackoverflow_url", url=url)

                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(2, 4))

                # Scroll to load more jobs
                for _ in range(1):
                    await page.evaluate("window.scrollBy(0, window.innerHeight)")
                    await asyncio.sleep(random.uniform(1, 2))

                # Extract job listings
                job_cards = await page.query_selector_all(".s-job-card")
                log.debug("stackoverflow_found_cards", count=len(job_cards))

                for card in job_cards[:max_results]:
                    try:
                        # Get job card link for URL
                        link_el = await card.query_selector(".s-link.stretched-link")
                        job_url = await link_el.get_attribute("href") if link_el else ""

                        # Get title
                        title_el = await card.query_selector(".s-link")
                        title = await title_el.inner_text() if title_el else "Unknown"

                        # Get company name
                        company_el = await card.query_selector(".mb4 .s-user-card--time")
                        company = await company_el.inner_text() if company_el else "Unknown"

                        # Get location and tags
                        location_els = await card.query_selector_all(".svg-icon-sm + span")
                        location_text = location
                        is_remote = False

                        if location_els:
                            for el in location_els:
                                text = await el.inner_text()
                                if text:
                                    location_text = text
                                    is_remote = "remote" in text.lower()
                                    if is_remote:
                                        break

                        external_id = self._make_external_id(
                            "stackoverflow", job_url or title
                        )

                        jobs.append(
                            JobCreate(
                                external_id=external_id,
                                title=title.strip(),
                                company=company.strip(),
                                location=location_text.strip(),
                                url=f"https://stackoverflow.com{job_url}"
                                if job_url
                                else "",
                                source="stackoverflow",
                                is_remote=is_remote,
                                raw_data={"source": "stackoverflow"},
                            )
                        )

                        log.debug(
                            "stackoverflow_job_parsed",
                            title=title,
                            company=company,
                        )

                    except Exception as e:
                        log.warning("stackoverflow_card_parse_error", error=str(e))
                        continue

                await browser.close()

        except Exception as e:
            log.error("stackoverflow_scrape_failed", error=str(e))

        log.info("stackoverflow_scrape_done", count=len(jobs))
        return jobs
