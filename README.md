# 🚀 AstroBot — AI Space Knowledge Chatbot

An AI-powered RAG (Retrieval-Augmented Generation) chatbot that answers questions about space, planets, NASA missions, black holes, dark matter, and everything in the cosmos — grounded in real NASA and astronomy data.

![AstroBot](https://img.shields.io/badge/AI-RAG%20Chatbot-blue) ![Python](https://img.shields.io/badge/Python-3.11-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal) ![React](https://img.shields.io/badge/React-18-blue) ![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

## ✨ Features
- 🤖 AI chatbot powered by LangChain RAG + HuggingFace FLAN-T5
- 🔍 ChromaDB vector database with 69 space knowledge documents
- 🪐 Complete solar system planet data from NASA
- 🛸 8 major NASA missions including JWST, Perseverance, Artemis
- 🌌 Deep space knowledge: black holes, dark matter, multiverse, time dilation
- ⚡ FastAPI REST backend with auto-generated docs
- 🗄️ MySQL database with full ORM
- 🎨 Professional dark space UI with animated starfield
- 🐳 Full Docker containerization

## 🏗️ Architecture

\\\
User Question
     ↓
React Frontend (port 3000)
     ↓
FastAPI Backend (port 8000)
     ↓
LangChain RAG Pipeline
     ↓
ChromaDB Vector Search → HuggingFace Embeddings
     ↓
FLAN-T5 LLM → Answer + Sources
     ↓
MySQL (planets, missions, chat history)
\\\

## 🚀 Quick Start with Docker

\\\ash
git clone https://github.com/CodeWithBigboss-source/Astrobot-RAG.git
cd Astrobot-RAG
docker-compose up --build
\\\

Open http://localhost:3000

## 🛠️ Local Development

\\\ash
# Backend
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm start
\\\

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/chat | Ask AstroBot a question |
| GET | /api/v1/planets | Get all planets |
| GET | /api/v1/planets/{name} | Get planet by name |
| GET | /api/v1/missions | Get all NASA missions |
| GET | /health | Health check |
| GET | /docs | Swagger UI |

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI/RAG | LangChain 0.2.5, HuggingFace FLAN-T5 |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | ChromaDB 0.5.3 |
| Backend | FastAPI 0.111, Python 3.11 |
| Database | MySQL 8.0, SQLAlchemy |
| Frontend | React 18, Axios |
| Container | Docker, docker-compose |
| ML | scikit-learn, numpy, pandas, matplotlib |

## 📁 Project Structure

\\\
astrobot-rag/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── routes/           # chat, planets endpoints
│   │   ├── models/           # SQLAlchemy + Pydantic
│   │   ├── rag/              # LangChain pipeline
│   │   └── data/             # NASA data ingestion
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # ChatBox, Planets, Missions, StarField
│   │   └── App.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
\\\

## 🌟 What I Learned
- Building end-to-end RAG pipelines with LangChain and ChromaDB
- HuggingFace transformers and sentence embeddings
- FastAPI with async endpoints, Pydantic validation, SQLAlchemy ORM
- React component architecture with real API integration
- Docker multi-container orchestration with docker-compose
- Vector database design and semantic search
- Professional Git workflow and project structure

## 👨‍💻 Author
Built by CodeWithBigboss | AI/ML Engineer in Training

---
⭐ Star this repo if you found it useful!
