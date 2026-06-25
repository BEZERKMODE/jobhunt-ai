# Job Portal Scrapers

Complete guide to JobHunt AI's multi-portal job scraping system.

## ✅ Currently Supported Portals

| Portal | Difficulty | Status | Notes |
|--------|-----------|--------|-------|
| **Indeed** | ✅ Easy | ✓ Active | Largest job board |
| **LinkedIn** | 🟡 Medium | ✓ Active | Requires delays/proxies |
| **Glassdoor** | 🟡 Medium | ✓ Active | Dynamic content |
| **Remote.co** | ✅ Easy | ✓ Active | Remote jobs only |
| **Stack Overflow** | ✅ Easy | ✓ Active | Developer jobs |

## 🏗️ Architecture

```
backend/app/services/scrapers/
├── base.py              # Abstract base class
├── registry.py          # Scraper manager
├── indeed.py            # Indeed implementation
├── linkedin.py          # LinkedIn implementation
├── glassdoor.py         # Glassdoor implementation
├── remoteco.py          # Remote.co implementation
├── stackoverflow.py     # Stack Overflow implementation
└── utils/
    ├── proxy.py         # Proxy rotation
    ├── delays.py        # Human-like delays
    └── __init__.py
```

## 🚀 How to Use

### Via API

```bash
# Scrape Indeed
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python Developer",
    "location": "San Francisco",
    "source": "indeed",
    "max_results": 20
  }'

# Scrape LinkedIn
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "Backend Engineer",
    "location": "Remote",
    "source": "linkedin",
    "max_results": 20
  }'

# Scrape Glassdoor
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "Data Scientist",
    "location": "New York",
    "source": "glassdoor",
    "max_results": 20
  }'

# Scrape Remote.co
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "Full Stack Developer",
    "source": "remoteco",
    "max_results": 20
  }'

# Scrape Stack Overflow
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "JavaScript",
    "location": "Berlin",
    "source": "stackoverflow",
    "max_results": 20
  }'
```

### Via Python

```python
from app.services.scrapers.registry import get_scraper

async def scrape_jobs():
    # Get any scraper
    scraper = get_scraper("indeed")
    
    # Run scrape
    jobs = await scraper.scrape(
        query="Python Developer",
        location="San Francisco",
        max_results=20
    )
    
    # Each job is a JobCreate object ready for DB
    for job in jobs:
        print(f"{job.title} at {job.company}")
        print(f"  URL: {job.url}")
        print(f"  Remote: {job.is_remote}")
```

## 🔧 Adding a New Scraper

### Step 1: Inspect the Target Website

```bash
# Open in browser and check:
1. Right-click → Inspect Element (F12)
2. Find job card selectors
3. Check for pagination
4. Look for anti-bot protection
```

### Step 2: Create Scraper File

**`backend/app/services/scrapers/mynewportal.py`**

```python
"""
MyNewPortal Jobs Scraper
"""

import asyncio
from typing import List
import structlog

from app.schemas import JobCreate
from app.services.scrapers.base import BaseJobScraper

log = structlog.get_logger()


class MyNewPortalScraper(BaseJobScraper):
    source_name = "mynewportal"
    BASE_URL = "https://mynewportal.com/jobs"

    async def scrape(
        self, query: str, location: str, max_results: int = 20
    ) -> List[JobCreate]:
        """Scrape MyNewPortal job listings."""
        from playwright.async_api import async_playwright

        jobs: List[JobCreate] = []
        log.info("mynewportal_scrape_start", query=query, location=location)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Build URL
                url = f"{self.BASE_URL}?q={query}&l={location}"
                
                # Navigate
                await page.goto(url, wait_until="domcontentloaded")

                # Find job cards
                job_cards = await page.query_selector_all(".job-card")

                for card in job_cards[:max_results]:
                    try:
                        # Extract data
                        title_el = await card.query_selector(".title")
                        company_el = await card.query_selector(".company")
                        
                        title = await title_el.inner_text() if title_el else "Unknown"
                        company = await company_el.inner_text() if company_el else "Unknown"

                        # Create job object
                        external_id = self._make_external_id("mynewportal", title)
                        
                        jobs.append(
                            JobCreate(
                                external_id=external_id,
                                title=title.strip(),
                                company=company.strip(),
                                location=location,
                                url="https://mynewportal.com/...",
                                source="mynewportal",
                                is_remote=False,
                            )
                        )

                    except Exception as e:
                        log.warning("mynewportal_parse_error", error=str(e))
                        continue

                await browser.close()

        except Exception as e:
            log.error("mynewportal_scrape_failed", error=str(e))

        log.info("mynewportal_scrape_done", count=len(jobs))
        return jobs
```

### Step 3: Register in Registry

**`backend/app/services/scrapers/registry.py`**

```python
from app.services.scrapers.mynewportal import MyNewPortalScraper

SCRAPER_REGISTRY: dict[str, type[BaseJobScraper]] = {
    # ...existing scrapers...
    "mynewportal": MyNewPortalScraper,
}
```

### Step 4: Test

```bash
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer TOKEN" \
  -d '{"query":"Python","location":"Remote","source":"mynewportal"}'
```

## 🛡️ Anti-Bot Measures

### 1. Realistic User Agent

```python
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
```

### 2. Random Delays

```python
from app.services.scrapers.utils import random_delay, page_load_delay

await page_load_delay()  # 2-8 seconds
await random_delay(2, 5)  # Between requests
```

### 3. Proxy Rotation

```python
from app.services.scrapers.utils import ProxyRotator

proxies = [
    "http://user:pass@proxy1.com:8080",
    "http://user:pass@proxy2.com:8080",
]
rotator = ProxyRotator(proxies)

browser = await p.chromium.launch(
    proxy={"server": rotator.random()}
)
```

### 4. Hide Webdriver

```python
await context.add_init_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => false})"
)
```

### 5. Realistic Viewport

```python
context = await browser.new_context(
    viewport={"width": 1920, "height": 1080}
)
```

## 📊 Return Format

All scrapers return `List[JobCreate]`:

```python
class JobCreate(BaseModel):
    external_id: str              # Unique hash to prevent duplicates
    title: str                    # Job title
    company: str                  # Company name
    location: str                 # Location
    description: str              # Job description
    url: str                      # Job link
    source: str                   # Scraper source (indeed, linkedin, etc.)
    is_remote: bool               # Is remote job?
    salary_min: Optional[int]     # Min salary in USD
    salary_max: Optional[int]     # Max salary in USD
    raw_data: Optional[dict]      # Extra metadata
```

## 🐛 Debugging

### Enable Logs

```bash
# See scraper logs
docker-compose logs -f backend | grep scrape
```

### Common Errors

**"net::ERR_CONNECTION_REFUSED"**
- Website is blocking your IP
- Solution: Use proxies, add delays

**"Timeout after 30000ms"**
- Page loads too slowly
- Solution: Increase timeout, check internet

**"Selector not found"**
- Website HTML changed
- Solution: Update selectors in scraper

## 📈 Performance Tips

1. **Use max_results=20-30** for balance between speed and coverage
2. **Add random delays** between 2-5 seconds
3. **Rotate user agents** for large-scale scraping
4. **Use residential proxies** for LinkedIn/Glassdoor
5. **Schedule scrapes** during off-peak hours
6. **Monitor rate limits** from each website

## 🚨 Legal & Ethical

- ✅ **Allowed**: Scraping public data, respecting robots.txt, adding delays
- ❌ **Not Allowed**: Bypassing authentication, DDoS attacks, republishing data

**Always check website's Terms of Service before scraping.**

## 📚 References

- [Playwright Docs](https://playwright.dev)
- [Indeed robots.txt](https://www.indeed.com/robots.txt)
- [LinkedIn robots.txt](https://www.linkedin.com/robots.txt)
- [Web Scraping Best Practices](https://help.apify.com/en/articles/3117563-best-practices-for-web-scraping)
