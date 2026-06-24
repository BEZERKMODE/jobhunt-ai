from abc import ABC, abstractmethod
from typing import List
from app.schemas import JobCreate


class BaseJobScraper(ABC):
    source_name: str = "base"

    @abstractmethod
    async def scrape(self, query: str, location: str, max_results: int = 20) -> List[JobCreate]:
        raise NotImplementedError

    def _make_external_id(self, source: str, unique_part: str) -> str:
        import hashlib
        raw = f"{source}:{unique_part}"
        return hashlib.sha256(raw.encode()).hexdigest()[:64]
