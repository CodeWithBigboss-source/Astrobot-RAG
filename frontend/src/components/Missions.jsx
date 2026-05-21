import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:8000/api/v1";

export default function Missions() {
  const [missions, setMissions] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState("");

  useEffect(() => {
    axios.get(`${API}/missions`)
      .then(r => { setMissions(r.data); setLoading(false); })
      .catch(() => { setError("Could not load missions. Is the backend running?"); setLoading(false); });
  }, []);

  if (loading) return <div className="loading"><span className="loading-icon">🛸</span>Loading missions...</div>;
  if (error)   return <div className="error">{error}</div>;

  return (
    <div>
      <div className="page-header">
        <h2 className="page-title">🛸 NASA Space Missions</h2>
        <p className="page-sub">Historic and active missions exploring our solar system and beyond</p>
      </div>
      <div className="cards">
        {missions.map(m => (
          <div key={m.id} className="card">
            <span className="card-icon">🚀</span>
            <h3>{m.name}</h3>
            <div className="badges">
              <span className={`badge ${m.status==="Active"?"badge-active":"badge-done"}`}>
                {m.status==="Active"?"🟢 Active":"✅ Completed"}
              </span>
              <span className="badge badge-purple">{m.agency}</span>
            </div>
            <p>{m.description?.slice(0,145)}...</p>
            <div className="stats">
              <div className="stat"><span className="stat-label">Target</span><span className="stat-value">{m.target}</span></div>
              <div className="stat"><span className="stat-label">Launch Date</span><span className="stat-value">{m.launch_date}</span></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}