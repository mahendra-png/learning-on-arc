from fastapi import FastAPI
from cache import cache
from logger import logger
from ai_service import get_ai_response 


app = FastAPI()

fake_db = {
    "1": {"id": 1, "title": "First Note", "content": "Hello Redis"},
    "2": {"id": 2, "title": "Second Note", "content": "FastAPI is great!"},
    "3": {"id": 3, "title": "Third Note", "content": "Caching with Redis"}
}

@app.get("/notes/{note_id}")
def get_note(note_id: int, user_id: int = 1):
    logger.info(f"Fetching note with ID: {note_id} for user ID: {user_id}")
    cache_key = f"user:{user_id}:note:{note_id}"
    note = cache.get(cache_key)
    if note:
        logger.info(f"Note found in cache for key: {cache_key}")
        return {"source": "cache", "note": note}
    logger.info(f"Note not found in cache for key: {cache_key}, fetching from database")
    note = fake_db.get(str(note_id))
    if note:
        logger.info(f"Note found in database for ID: {note_id}, caching result")
        cache.set(cache_key, note)
        return {"source": "database", "note": note}
    logger.warning(f"Note with ID: {note_id} not found in database")
    return {"error": "Note not found"}

@app.get("/ai")
def ai_response(prompt: str):
    return get_ai_response(prompt)  
 


