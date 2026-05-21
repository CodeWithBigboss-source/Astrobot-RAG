from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, planets
from app.models.database import create_tables, SessionLocal
from app.data.ingest import load_planets_to_db, load_missions_to_db
from app.rag.vectorstore import vectorstore_exists, build_vectorstore
from app.data.ingest import get_all_documents
import uvicorn

app = FastAPI(
    title="AstroBot API",
    description="AI-powered space knowledge chatbot using RAG, LangChain, HuggingFace & ChromaDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(planets.router, prefix="/api/v1", tags=["Planets & Missions"])

@app.on_event("startup")
async def startup_event():
    print("AstroBot starting up...")
    # Create MySQL tables
    create_tables()
    # Seed database
    db = SessionLocal()
    try:
        load_planets_to_db(db)
        load_missions_to_db(db)
    finally:
        db.close()
    # Build vector store if not exists
    if not vectorstore_exists():
        print("First run: building ChromaDB vector store...")
        documents = get_all_documents()
        build_vectorstore(documents)
    print("AstroBot ready!")

@app.get("/")
def root():
    return {
        "message": "Welcome to AstroBot API!",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "AstroBot RAG API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)