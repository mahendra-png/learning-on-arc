from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from rag_service import RAGService

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_document/")
def add_document(content: str, doc_id: int, db: Session = Depends(get_db)):
    rag_service = RAGService(db)
    rag_service.add_document(content, doc_id)
    return {"message": "Document added successfully"}

@app.get("/query/")
def query(question: str, db: Session = Depends(get_db)):
    rag_service = RAGService(db)
    results = rag_service.query(question)
    return {"results": results}
