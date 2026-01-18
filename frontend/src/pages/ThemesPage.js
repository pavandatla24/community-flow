import { useEffect, useState } from "react";
import { apiGet } from "../services/api";
import JsonBlock from "../components/JsonBlock";

export default function ThemesPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet("/themes")
      .then(setData)
      .catch((e) => setError(e.message || "Failed to load"));
  }, []);

  return (
    <div>
      <h2>Themes</h2>
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
      {data ? <JsonBlock data={data} /> : <p>Loading...</p>}
    </div>
  );
}
