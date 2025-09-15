import redis.asyncio as redis
import json
import hashlib
from config.settings import settings
from config.logger import logger

# Create a single, reusable connection pool to Redis
try:
    redis_pool = redis.ConnectionPool.from_url(settings.redis_url, decode_responses=True)
    logger.info("Successfully created Redis connection pool for caching.")
except Exception as e:
    logger.error(f"Failed to create Redis connection pool for caching: {e}")
    redis_pool = None

def create_cache_key(question: str) -> str:
    """Creates a consistent, hashed key for a given question."""
    return f"nlq_cache:{hashlib.md5(question.encode()).hexdigest()}"

async def get_from_cache(key: str) -> dict | None:
    """Retrieves a result from the Redis cache."""
    if not redis_pool:
        return None
    try:
        r = redis.Redis(connection_pool=redis_pool)
        cached_result = await r.get(key)
        if cached_result:
            logger.info(f"Cache HIT for key: {key}")
            return json.loads(cached_result)
        logger.info(f"Cache MISS for key: {key}")
        return None
    except Exception as e:
        logger.error(f"Error getting from Redis cache: {e}")
        return None

async def set_to_cache(key: str, value: dict):
    """Saves a result to the Redis cache with a timeout."""
    if not redis_pool:
        return
    try:
        r = redis.Redis(connection_pool=redis_pool)
        value_json = json.dumps(value, default=str)
        # Use the cache_ttl from settings (e.g., 3600 seconds = 1 hour)
        await r.setex(key, settings.cache_ttl, value_json)
        logger.info(f"Successfully set cache for key: {key}")
    except Exception as e:
        logger.error(f"Error setting to Redis cache: {e}")