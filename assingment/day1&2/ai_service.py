import hashlib
from cache import cache
from logger import logger

def get_ai_response(prompt: str) -> str:
    logger.info(f"Generating AI response for prompt: {prompt}")
    cache_key = f"airesponse:{hashlib.md5(prompt.encode()).hexdigest()}"
    cached_response = cache.get(cache_key)
    if cached_response:
        logger.info(f"AI response found in cache for key: {cache_key}")
        return {"source": "cache", "response": cached_response}
    logger.info(f"AI response not found in cache for key: {cache_key}, generating new response")
    reaponse = f"AI response to: {prompt}"
    cache.set(cache_key, reaponse, ttl=3600)
    logger.info(f"AI response generated and cached for key: {cache_key}")
    return {"source": "AI", "response": reaponse}
