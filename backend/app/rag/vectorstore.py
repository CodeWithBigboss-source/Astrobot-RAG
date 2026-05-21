from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.rag.embedder import get_embeddings
import os

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

def build_vectorstore(documents: list) -> Chroma:
    """Build and persist ChromaDB vector store from documents."""
    embeddings = get_embeddings()
    docs = [
        Document(
            page_content=doc["content"],
            metadata={"source": doc["source"], "type": doc["type"]}
        )
        for doc in documents
    ]
    print(f"Building vector store with {len(docs)} documents...")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="astrobot_space_knowledge"
    )
    vectorstore.persist()
    print(f"Vector store built and saved to {CHROMA_DIR}")
    return vectorstore

def load_vectorstore() -> Chroma:
    """Load existing ChromaDB vector store from disk."""
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_name="astrobot_space_knowledge"
    )
    return vectorstore

def vectorstore_exists() -> bool:
    """Check if a persisted vector store already exists."""
    chroma_sqlite = os.path.join(CHROMA_DIR, "chroma.sqlite3")
    return os.path.exists(chroma_sqlite)