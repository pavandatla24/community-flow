import { useEffect, useState } from "react";
import { apiGet } from "./services/api";

function App() {
  const [health, setHealth] = useState(null);
  const [themesData, setThemesData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const h = await apiGet("/health");
        setHealth(h);

        const t = await apiGet("/themes");
        setThemesData(t);
      } catch (e) {
        setError(e.message || String(e));
      }
    }
    load();
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>Community Flow</h1>

      {error ? (
        <div style={{ color: "red" }}>
          <h3>Error</h3>
          <pre>{error}</pre>
          <p>
            Make sure backend is running on <code>127.0.0.1:8000</code> and CORS
            is enabled.
          </p>
        </div>
      ) : (
        <>
          <h3>Backend Health</h3>
          <pre>{health ? JSON.stringify(health, null, 2) : "Loading..."}</pre>

          <h3>Themes Summary</h3>
          <pre>
            {themesData ? JSON.stringify(themesData, null, 2) : "Loading..."}
          </pre>
        </>
      )}
    </div>
  );
}

export default App;
