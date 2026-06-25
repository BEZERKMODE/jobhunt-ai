"""
LinkedIn Jobs Scraper using Playwright.
Note: LinkedIn has strict anti-bot measures. Use realistic delays and headers.
"""

import asyncio
import random
from typing import List
import structlog

from app.schemas import JobCreate
from app.services.scrapers.base import BaseJobScraper

log = structlog.get_logger()


class LinkedInScraper(BaseJobScraper):
    source_name = "linkedin"
    BASE_URL = "https://www.linkedin.com/jobs/search"

    async def scrape(
        self, query: str, location: str, max_results: int = 20
    ) -> List[JobCreate]:
        """
        Scrape LinkedIn jobs.

        ⚠️ LinkedIn blocks bots aggressively. For production:
        - Use rotating residential proxies
        - Add random delays between requests
        """
        from playwright.async_api import async_playwright

        jobs: List[JobCreate] = []
        log.info("linkedin_scrape_start", query=query, location=location)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-blink-features=AutomationControlled",
                    ],
                )

                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                    viewport={"width": 1920, "height": 1080},
                )

                # Hide webdriver property
                await context.add_init_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => false})"
                )

                page = await context.new_page()

                # Build LinkedIn job search URL
                params = {
                    "keywords": query,
                    "location": location,
                    "distance": "25",
                    "f_AL": "true",  # Available now
                    "f_JT": "F,C,T",  # Full-time, Contract, Temporary
                }
                url = f"{self.BASE_URL}?" + "&".join(f"{k}={v}" for k, v in params.items())

                log.debug("linkedin_url", url=url)

                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(2, 4))

                # Scroll to load jobs dynamically
                for _ in range(2):
                    await page.evaluate("window.scrollBy(0, window.innerHeight)")
                    await asyncio.sleep(random.uniform(1, 2))

                # Extract job listings
                job_cards = await page.query_selector_all("li[data-job-id]")
                log.debug("linkedin_found_cards", count=len(job_cards))

                for card in job_cards[:max_results]:
                    try:
                        job_id = await card.get_attribute("data-job-id")

                        # Click to open job details
                        await card.click()
                        await asyncio.sleep(random.uniform(1, 2))

                        # Get job details from right panel
                        title_el = await page.query_selector(
                            ".top-card-layout__title"
                        )
                        company_el = await page.query_selector(
                            ".top-card-layout__company-name"
                        )
                        location_el = await page.query_selector(
                            ".job-details-jobs-unified-top-card__job-insight"
                        )
                        description_el = await page.query_selector(
                            ".show-more-less-html__markup"
                        )

                        title = await title_el.inner_text() if title_el else "Unknown"
                        company = (
                            await company_el.inner_text() if company_el else "Unknown"
                        )
                        location_text = (
                            await location_el.inner_text()
                            if location_el
                            else location
                        )
                        description = (
                            await description_el.inner_text()
                            if description_el
                            else ""
                        )

                        job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
                        external_id = self._make_external_id("linkedin", job_id or title)

                        is_remote = (
                            "remote" in location_text.lower()
                            or "anywhere" in location_text.lower()
                        )

                        jobs.append(
                            JobCreate(
                                external_id=external_id,
                                title=title.strip(),
                                company=company.strip(),
                                location=location_text.strip(),
                                description=description.strip(),
                                url=job_url,
                                source="linkedin",
                                is_remote=is_remote,
                                raw_data={"job_id": job_id},
                            )
                        )

                        log.debug(
                            "linkedin_job_parsed",
                            title=title,
                            company=company,
                        )

                    except Exception as e:
                        log.warning("linkedin_card_parse_error", error=str(e))
                        continue

                await browser.close()

        except Exception as e:
            log.error("linkedin_scrape_failed", error=str(e))

        log.info("linkedin_scrape_done", count=len(jobs))
        return jobs
