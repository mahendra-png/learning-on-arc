from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector
from database import Base

class DocumnetChunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer)
    content = Column(Text)
    embedding = Column(Vector(384))
    
