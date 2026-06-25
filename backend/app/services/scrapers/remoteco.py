"""
Remote.co Jobs Scraper - Remote-only job listings.
Remote.co aggregates remote jobs from various sources.
"""

import asyncio
import random
from typing import List
import structlog

from app.schemas import JobCreate
from app.services.scrapers.base import BaseJobScraper

log = structlog.get_logger()


class RemoteCoScraper(BaseJobScraper):
    source_name = "remoteco"
    BASE_URL = "https://remote.co/remote-jobs"

    async def scrape(
        self, query: str, location: str, max_results: int = 20
    ) -> List[JobCreate]:
        """
        Scrape Remote.co remote job listings.
        All jobs are inherently remote, so location filter is ignored.
        """
        from playwright.async_api import async_playwright

        jobs: List[JobCreate] = []
        log.info("remoteco_scrape_start", query=query)

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

                # Remote.co search by category
                category_slug = query.lower().replace(" ", "-")
                url = f"{self.BASE_URL}/{category_slug}"

                log.debug("remoteco_url", url=url)

                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(random.uniform(2, 4))

                # Scroll to load more jobs
                for _ in range(2):
                    await page.evaluate("window.scrollBy(0, window.innerHeight)")
                    await asyncio.sleep(random.uniform(1, 2))

                # Extract job listings
                job_cards = await page.query_selector_all(".job-listing")
                log.debug("remoteco_found_cards", count=len(job_cards))

                for card in job_cards[:max_results]:
                    try:
                        title_el = await card.query_selector(".job-title a")
                        company_el = await card.query_selector(".company-name")
                        link_el = await card.query_selector(".job-title a")
                        tags_el = await card.query_selector_all(".job-tag")

                        title = await title_el.inner_text() if title_el else "Unknown"
                        company = (
                            await company_el.inner_text()
                            if company_el
                            else "Remote.co"
                        )
                        job_url = await link_el.get_attribute("href") if link_el else ""

                        # Extract salary if available from tags
                        salary_text = None
                        for tag in tags_el:
                            text = await tag.inner_text()
                            if "$" in text:
                                salary_text = text
                                break

                        external_id = self._make_external_id("remoteco", job_url or title)

                        jobs.append(
                            JobCreate(
                                external_id=external_id,
                                title=title.strip(),
                                company=company.strip(),
                                location="Remote",
                                url=f"https://remote.co{job_url}"
                                if job_url
                                else "https://remote.co",
                                source="remoteco",
                                is_remote=True,
                                raw_data={"source": "remote.co"},
                            )
                        )

                        log.debug("remoteco_job_parsed", title=title, company=company)

                    except Exception as e:
                        log.warning("remoteco_card_parse_error", error=str(e))
                        continue

                await browser.close()

        except Exception as e:
            log.error("remoteco_scrape_failed", error=str(e))

        log.info("remoteco_scrape_done", count=len(jobs))
        return jobs
