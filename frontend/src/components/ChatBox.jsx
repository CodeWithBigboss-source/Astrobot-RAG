import { useState, useRef, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:8000/api/v1";

const SUGGESTIONS = [
  "What is a black hole and how does it form?",
  "Tell me about the James Webb Space Telescope",
  "How does time dilation work in space?",
  "What is dark matter and dark energy?",
  "Are there other Earth-like planets?",
  "What happened during the Big Bang?",
  "Explain how gravitational waves work",
  "What is the multiverse theory?",
];

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async (q) => {
    const question = q || input.trim();
    if (!question || loading) return;
    setInput("");
    setMessages(p => [...p, { role: "user", text: question }]);
    setLoading(true);
    try {
      const res = await axios.post(`${API}/chat`, { question });
      setMessages(p => [...p, { role: "bot", text: res.data.answer, sources: res.data.sources }]);
    } catch {
      setMessages(p => [...p, { role: "bot", text: "Connection error. Is the backend running on port 8000?", sources: [] }]);
    }
    setLoading(false);
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.length === 0 && (
          <div className="welcome">
            <span className="welcome-icon">🔭</span>
            <h2>Welcome to AstroBot</h2>
            <p>I'm your AI-powered guide to the cosmos. Ask me about black holes, dark matter, exoplanets, NASA missions, time dilation, the multiverse — anything space.</p>
            <div className="suggestions">
              {SUGGESTIONS.map(s => (
                <button key={s} className="suggestion-btn" onClick={() => send(s)}>{s}</button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <div className="msg-label">{m.role === "user" ? "You" : "🚀 AstroBot"}</div>
            <div className="bubble">{m.text}</div>
            {m.sources?.length > 0 && (
              <div className="sources">
                📚
                {m.sources.map(s => <span key={s} className="source-chip">{s}</span>)}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="thinking">
            <span>🔭 AstroBot is thinking</span>
            <div className="dot-pulse"><span/><span/><span/></div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send()}
          placeholder="Ask anything about space, planets, stars, black holes..."
          disabled={loading}
        />
        <button onClick={() => send()} disabled={loading}>
          {loading ? "..." : "Ask 🚀"}
        </button>
      </div>
    </div>
  );
}