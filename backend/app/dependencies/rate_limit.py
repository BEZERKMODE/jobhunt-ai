from fastapi import Request, HTTPException
import redis.asyncio as aioredis
from app.core.redis import redis_client


async def rate_limit(request: Request, key: str, limit: int = 10, window: int = 60):
    """Simple sliding window rate limiter using Redis INCR+EXPIRE."""
    r_key = f"ratelimit:{key}:{request.client.host}"
    count = await redis_client.incr(r_key)
    if count == 1:
        await redis_client.expire(r_key, window)
    if count > limit:
        raise HTTPException(status_code=429, detail="Too many requests")
