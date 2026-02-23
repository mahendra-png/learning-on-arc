from models import DocumnetChunk
from embedding_service import EmbeddingService
from sqlalchemy import text

class RAGService:
    def __init__(self, db):
        self.db = db
        self.embedding_service = EmbeddingService()
    
    def split_text(self, text, chunk_size=500):
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append(chunk)

        return chunks
    
    def add_document(self, contant, doc_id):
        chunks = self.split_text(contant)
        for chunk in chunks:
            embedding = self.embedding_service.embed(chunk)
            doc_chunk = DocumnetChunk(
                document_id=doc_id,
                content=chunk,
                embedding=embedding
            )
            self.db.add(doc_chunk)
        self.db.commit()
    
    def query(self, question):
        query_embedding = self.embedding_service.embed(question)

        results = self.db.execute(
            text("""
            SELECT content
            FROM chunks
            ORDER BY embedding <=> (:embedding)::vector
            LIMIT 5
        """),
            {"embedding": query_embedding}
        ).fetchall()

        formatted_results = [row[0] for row in results]

        return formatted_results
