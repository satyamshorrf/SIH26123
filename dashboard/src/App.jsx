import { useEffect, useState } from "react";

function App() {
  const [robots, setRobots] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/robots")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend unavailable");
        }
        return response.json();
      })
      .then((data) => {
        setRobots(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>EdgeFleet Dashboard</h1>

      {error && <p>{error}</p>}

      {Object.entries(robots).map(([id, robot]) => (
        <div
          key={id}
          style={{
            border: "1px solid #ccc",
            padding: "15px",
            margin: "10px 0",
            borderRadius: "10px",
          }}
        >
          <h2>{id}</h2>

          <p>
            Position: ({robot.x}, {robot.y})
          </p>

          <p>Battery: {robot.battery}%</p>

          <p>Status: {robot.status}</p>
        </div>
      ))}
    </div>
  );
}

export default App;