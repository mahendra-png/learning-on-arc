from asyncio.log import logger
import redis
import json
from logger import logger

class RedisCache:
    def __init__(self):
        self.client = redis.from_url("redis://redis:6379/0")
        logger.info("Connected to Redis")

    def set(self, key, value, ttl=300):
        try:
            self.client.setex(key, ttl, json.dumps(value))
            logger.info(f"Set cache for key: {key} with TTL: {ttl} seconds")
        except Exception as e:
            logger.error(f"Error setting cache for key: {key} - {e}")
        
    def get(self, key):
        try:
            value = self.client.get(key)
            if value is not None:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(value)
            else:
                logger.info(f"Cache miss for key: {key}")
                return None
        except Exception as e:
            logger.error(f"Error getting cache for key: {key} - {e}")
            return None
    
    def delete(self, key):
        try:
            self.client.delete(key)
            logger.info(f"Deleted cache for key: {key}")
        except Exception as e:
            logger.error(f"Error deleting cache for key: {key} - {e}")

cache = RedisCache()
