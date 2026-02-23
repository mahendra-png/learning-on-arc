from fastapi import Depends, FastAPI
from app.database.session import engine
from app.database.base import Base
from app.routes import auth
from app.core.security import get_current_user
from sqlalchemy import text
from app.routes import document
from app.routes import qa
from app.services.ai_service import AIService


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(document.router)
app.include_router(qa.router)
ai_service = AIService()


@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected route"}

with engine.connect() as connection:
    connection.execute(text("SELECT 1"))
    print("Database connection successful")

