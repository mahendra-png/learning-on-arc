from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATSBASE_URL = "postgresql://postgres:pass@localhost:5432/ai_db"

engine = create_engine(DATSBASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
