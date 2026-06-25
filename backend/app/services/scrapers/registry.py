from app.services.scrapers.base import BaseJobScraper
from app.services.scrapers.indeed import IndeedScraper
from app.services.scrapers.linkedin import LinkedInScraper
from app.services.scrapers.glassdoor import GlassdoorScraper
from app.services.scrapers.remoteco import RemoteCoScraper
from app.services.scrapers.stackoverflow import StackOverflowScraper

SCRAPER_REGISTRY: dict[str, type[BaseJobScraper]] = {
    "indeed": IndeedScraper,
    "linkedin": LinkedInScraper,
    "glassdoor": GlassdoorScraper,
    "remoteco": RemoteCoScraper,
    "stackoverflow": StackOverflowScraper,
}


def get_scraper(source: str) -> BaseJobScraper:
    cls = SCRAPER_REGISTRY.get(source)
    if not cls:
        available = list(SCRAPER_REGISTRY.keys())
        raise ValueError(f"Unknown scraper '{source}'. Available: {available}")
    return cls()
