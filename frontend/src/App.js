import { useState } from "react";
import ChatBox from "./components/ChatBox";
import Planets from "./components/Planets";
import Missions from "./components/Missions";
import StarField from "./components/StarField";
import "./App.css";

export default function App() {
  const [page, setPage] = useState("chat");
  return (
    <div className="app">
      <StarField />
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">🚀</span>
            <span className="logo-text">AstroBot</span>
            <span className="logo-badge">AI</span>
          </div>
          <p className="tagline">Your AI guide to the cosmos — powered by NASA data & RAG</p>
          <nav className="nav">
            {[["chat","💬","Ask AstroBot"],["planets","🪐","Planets"],["missions","🛸","Missions"]].map(([id,icon,label])=>(
              <button key={id} className={page===id?"nav-btn active":"nav-btn"} onClick={()=>setPage(id)}>
                <span>{icon}</span><span>{label}</span>
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="main">
        {page==="chat"    && <ChatBox />}
        {page==="planets" && <Planets />}
        {page==="missions"&& <Missions />}
      </main>
      <footer className="footer">
        <span>Built with</span>
        {["LangChain","HuggingFace","ChromaDB","FastAPI","MySQL","React"].map(t=>(
          <span key={t} className="tech-badge">{t}</span>
        ))}
      </footer>
    </div>
  );
}