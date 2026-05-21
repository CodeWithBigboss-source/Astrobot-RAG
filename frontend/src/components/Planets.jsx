import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:8000/api/v1";
const ICONS = { Terrestrial:"🌍", "Gas Giant":"🪐", "Ice Giant":"🔵" };
const COLORS = { Terrestrial:"badge-active", "Gas Giant":"badge-purple", "Ice Giant":"badge-type" };

export default function Planets() {
  const [planets, setPlanets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState("");

  useEffect(() => {
    axios.get(`${API}/planets`)
      .then(r => { setPlanets(r.data); setLoading(false); })
      .catch(() => { setError("Could not load planets. Is the backend running?"); setLoading(false); });
  }, []);

  if (loading) return <div className="loading"><span className="loading-icon">🪐</span>Loading planets...</div>;
  if (error)   return <div className="error">{error}</div>;

  return (
    <div>
      <div className="page-header">
        <h2 className="page-title">🪐 Solar System Planets</h2>
        <p className="page-sub">Explore all 8 planets from our NASA-sourced knowledge base</p>
      </div>
      <div className="cards">
        {planets.map(p => (
          <div key={p.id} className="card">
            <span className="card-icon">{ICONS[p.type] || "🌑"}</span>
            <h3>{p.name}</h3>
            <div className="badges">
              <span className={`badge ${COLORS[p.type] || "badge-type"}`}>{p.type}</span>
            </div>
            <p>{p.description?.slice(0,140)}...</p>
            <div className="stats">
              <div className="stat"><span className="stat-label">Distance from Sun</span><span className="stat-value">{p.distance_from_sun}M km</span></div>
              <div className="stat"><span className="stat-label">Orbital Period</span><span className="stat-value">{p.orbital_period} Earth days</span></div>
              <div className="stat"><span className="stat-label">Moons</span><span className="stat-value">{p.moons}</span></div>
              <div className="stat"><span className="stat-label">Radius</span><span className="stat-value">{p.radius?.toLocaleString()} km</span></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}