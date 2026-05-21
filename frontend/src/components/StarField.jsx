import { useMemo } from "react";

export default function StarField() {
  const stars = useMemo(() => Array.from({ length: 160 }, (_, i) => ({
    id: i,
    left:    `${Math.random() * 100}%`,
    top:     `${Math.random() * 100}%`,
    size:    Math.random() * 2.5 + 0.5,
    dur:     `${Math.random() * 4 + 2}s`,
    delay:   `${Math.random() * 5}s`,
    opacity: Math.random() * 0.5 + 0.2,
  })), []);

  return (
    <div className="starfield">
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />
      {stars.map(s => (
        <div key={s.id} className="star" style={{
          left: s.left, top: s.top,
          width: s.size, height: s.size,
          "--dur": s.dur, "--delay": s.delay, "--opacity": s.opacity
        }} />
      ))}
    </div>
  );
}