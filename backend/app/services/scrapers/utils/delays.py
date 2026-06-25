"""
Delay utilities to simulate human-like behavior during scraping.
"""

import asyncio
import random


async def random_delay(min_sec: float = 1, max_sec: float = 5):
    """Sleep for a random duration to simulate human behavior."""
    delay = random.uniform(min_sec, max_sec)
    await asyncio.sleep(delay)


async def typing_delay(chars: int = 20):
    """Simulate typing speed (0.05-0.1 seconds per character)."""
    delay = random.uniform(0.05, 0.1) * chars
    await asyncio.sleep(delay)


async def page_load_delay():
    """Simulate reading a page (2-8 seconds)."""
    await random_delay(2, 8)


async def request_delay():
    """Delay between requests (2-5 seconds)."""
    await random_delay(2, 5)


async def page_navigation_delay():
    """Delay after page navigation (3-6 seconds)."""
    await random_delay(3, 6)


# Usage example:
# from app.services.scrapers.utils.delays import random_delay, page_load_delay
#
# await page_load_delay()  # Wait before scraping
# await random_delay(2, 4)  # Between requests
# await typing_delay(len("search term"))  # When typing
