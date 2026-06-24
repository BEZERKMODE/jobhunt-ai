from app.services.scrapers.base import BaseJobScraper
from app.services.scrapers.indeed import IndeedScraper

SCRAPER_REGISTRY: dict[str, type[BaseJobScraper]] = {
    "indeed": IndeedScraper,
}


def get_scraper(source: str) -> BaseJobScraper:
    cls = SCRAPER_REGISTRY.get(source)
    if not cls:
        available = list(SCRAPER_REGISTRY.keys())
        raise ValueError(f"Unknown scraper '{source}'. Available: {available}")
    return cls()
