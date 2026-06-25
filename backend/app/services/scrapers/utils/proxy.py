"""
Proxy rotation utilities for respectful scraping.
"""

import random
from typing import Optional


class ProxyRotator:
    """Rotate through proxy list to avoid IP blocking."""

    def __init__(self, proxies: list[str]):
        self.proxies = proxies
        self.current = 0

    def next(self) -> Optional[str]:
        """Get next proxy in rotation."""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current]
        self.current = (self.current + 1) % len(self.proxies)
        return proxy

    def random(self) -> Optional[str]:
        """Get random proxy from list."""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def reset(self):
        """Reset rotation counter."""
        self.current = 0


# Example usage:
# proxies = [
#     "http://user:pass@proxy1.com:8080",
#     "http://user:pass@proxy2.com:8080",
#     "http://user:pass@proxy3.com:8080",
# ]
# rotator = ProxyRotator(proxies)
#
# browser = await p.chromium.launch(
#     proxy={"server": rotator.random()}
# )
