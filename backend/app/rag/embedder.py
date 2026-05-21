from langchain_huggingface import HuggingFaceEmbeddings
import os

def get_embeddings():
    """Load HuggingFace sentence-transformer embedding model."""
    model_name = os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    print(f"Loading embedding model: {model_name}")
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    print("Embedding model loaded successfully.")
    return embeddings