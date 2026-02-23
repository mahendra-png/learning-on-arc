from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.core.security import get_current_user
from app.models.chunk import Chunk
from app.services.embedding_service import EmbeddingService
# import get_embedding, cosine_similarity
# get_embedding, cosine_similarity
import json
from pydantic import BaseModel
from sqlalchemy import text

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
# def ask_question(question: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
def ask_question(request: QuestionRequest, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    question = request.question
    embedding_service = EmbeddingService()
    question_embedding = embedding_service.get_embedding(question)
    print("Question embedding length:", len(question_embedding))
    
    # chunks = db.query(Chunk).all()

    # scored_chunks = []

    # for chunk in chunks:
    #     chunk_embedding = chunk.embedding
    #     print("Chunk embedding length:", len(chunk_embedding))
    #     if len(chunk_embedding) != len(question_embedding):
    #         print(f"Skipping chunk {chunk.id} due to embedding length mismatch")
    #         continue
    #     similarity = embedding_service.cosine_similarity(question_embedding, chunk_embedding)
    #     scored_chunks.append((similarity, chunk.content))
        
    # scored_chunks.sort(reverse=True)
    # top_chunks = [content for _, content in scored_chunks[:3]]

    # context = "\n".join(top_chunks)

    # results = db.query(Chunk).order_by(
    #     text("embedding <=> :query_embedding")
    # ).params(query_embedding=question_embedding).limit(3).all()

    results = db.query(Chunk).order_by(
        Chunk.embedding.cosine_distance(question_embedding)
    ).limit(3).all()

    # results = db.query(Chunk).order_by(
    #     Chunk.embedding.cosine_distance(question_embedding)
    # ).limit(3).all()

    if not results:
        return {"answer": "No relevant information found in the documents."}    
    context = "\n".join([chunk.content for chunk in results])

    
    return {"answer": f"Based on the context: {context}, the answer to your question '{question}' is: [Simulated Answer]"}