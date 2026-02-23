from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.document import Document
from app.core.security import get_current_user
from app.models.chunk import Chunk
import json
from app.services.embedding_service import EmbeddingService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def split_text(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    current_user: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    content = await file.read()
    text_content = content.decode("utf-8")
    
    document = Document(filename=file.filename, owner_id=current_user.id)
    db.add(document)
    db.commit()
    db.refresh(document)
    
    chunks = split_text(text_content)
    
    for chunk in chunks:
        # fake_embedding = [0.1] * 10
        fake_embedding = EmbeddingService.get_embedding(chunk)
        chunk_entry = Chunk(content=chunk, embedding=json.dumps(fake_embedding), document_id=document.id)
        db.add(chunk_entry)
        fake_embedding = json.dumps(fake_embedding)
    
    db.commit()
    
    return {"message": "Document uploaded successfully", "document_id": document.id}