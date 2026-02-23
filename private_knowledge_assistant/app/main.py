from fastapi import FastAPI, UploadFile, File
import shutil
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PDFService
from app.services.rag_service import RAGServices
from app.services.vector_service import VectorService
from pydantic import BaseModel


app = FastAPI()

chunk_service = ChunkService()
embedding_service = EmbeddingService()
pdf_service = PDFService()
rag_service = RAGServices()
vector_service = None

class QuestionRequest(BaseModel):
    question: str


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = pdf_service.extract_text(file_path)
    chunks = chunk_service.split_text(text)
    embeddings = embedding_service.embed(chunks)

    global vector_service
    vector_service = VectorService(len(embeddings[0]))
    vector_service.add(embeddings, chunks)

    return {"message": "PDF processed successfully"}

@app.post("/ask/")
def ask_question(request: QuestionRequest):
    if vector_service is None:
        return {"status": False, "msg": "No documnet uploaded yet. Please upload PDF first"}
    question = request.question

    query_embedding = embedding_service.embed([question])[0]
    contexts = vector_service.search(query_embedding)

    combined_context = "\n\n".join(contexts)
    answer = rag_service.generte(combined_context, question)

    return {"answer": answer}
    