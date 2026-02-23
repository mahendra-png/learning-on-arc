from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.base import Base
from pgvector.sqlalchemy import Vector

class Chunk(Base):
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    embedding = Column(Vector(384))
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    document = relationship("Document", back_populates="chunk")