import { useEffect, useState } from "react";

function CursorTrail() {
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const move = (e) => {
      setPos({
        x: e.clientX,
        y: e.clientY,
      });
    };

    window.addEventListener("mousemove", move);

    return () => {
      window.removeEventListener("mousemove", move);
    };
  }, []);

  return (
    <div
      className="cursor-trail"
      style={{
        left: pos.x,
        top: pos.y,
      }}
    />
  );
}

export default CursorTrail;