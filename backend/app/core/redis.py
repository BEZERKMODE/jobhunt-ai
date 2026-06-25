import os
import redis.asyncio as aioredis
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Async client for use in FastAPI (websockets, background async code)
redis_client = aioredis.from_url(REDIS_URL)

# Synchronous client for use in Celery workers / sync tasks
redis_sync = redis.from_url(REDIS_URL)
