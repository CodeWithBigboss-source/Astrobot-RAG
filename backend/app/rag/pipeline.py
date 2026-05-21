from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline as hf_pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from app.rag.vectorstore import load_vectorstore, build_vectorstore, vectorstore_exists
from app.data.ingest import get_all_documents
import torch

PROMPT_TEMPLATE = """You are AstroBot, an expert AI assistant specialized in space science, astronomy, and NASA missions.
Use the following context from our space knowledge base to answer the question accurately and engagingly.
If the context does not contain enough information, say so honestly — do not make up facts.

Context:
{context}

Question: {question}

Answer as AstroBot (be informative, engaging, and accurate):"""

PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

_qa_chain = None

def get_llm():
    """Load a lightweight CPU-friendly LLM (FLAN-T5-base)."""
    print("Loading LLM: google/flan-t5-base (CPU-optimized)...")
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    pipe = hf_pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        device=-1  # CPU
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    print("LLM loaded successfully.")
    return llm

def get_qa_chain():
    """Initialize or return existing RAG QA chain (singleton)."""
    global _qa_chain
    if _qa_chain is not None:
        return _qa_chain

    # Build or load vector store
    if vectorstore_exists():
        print("Loading existing vector store...")
        vectorstore = load_vectorstore()
    else:
        print("Building new vector store from space data...")
        documents = get_all_documents()
        vectorstore = build_vectorstore(documents)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    llm = get_llm()

    _qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    print("RAG QA chain ready.")
    return _qa_chain

def ask_astrobot(question: str) -> dict:
    """Run a question through the RAG pipeline and return answer + sources."""
    chain = get_qa_chain()
    result = chain.invoke({"query": question})
    answer = result.get("result", "I could not find an answer to that question.")
    source_docs = result.get("source_documents", [])
    sources = list({doc.metadata.get("source", "Unknown") for doc in source_docs})
    return {"answer": answer, "sources": sources}