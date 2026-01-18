// import { useEffect, useState } from "react";
// import { apiGet } from "../services/api";
// import JsonBlock from "../components/JsonBlock";

// export default function MapPage() {
//   const [data, setData] = useState(null);
//   const [error, setError] = useState("");

//   useEffect(() => {
//     apiGet("/map-data")
//       .then(setData)
//       .catch((e) => setError(e.message || "Failed to load"));
//   }, []);

//   return (
//     <div>
//       <h2>Map Data</h2>
//       {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
//       {data ? <JsonBlock data={data} /> : <p>Loading...</p>}
//     </div>
//   );
// }

// frontend/src/pages/MapPage.js

import React, { useEffect, useState } from "react";
import { api } from "../services/api";

export default function MapPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        setLoading(true);
        setError("");
        const res = await api.mapData();
        if (!mounted) return;
        setData(res);
      } catch (e) {
        if (!mounted) return;
        setError(e.message || "Failed to load map data");
      } finally {
        if (!mounted) return;
        setLoading(false);
      }
    }

    load();
    return () => (mounted = false);
  }, []);

  if (loading) return <div style={styles.page}>Loading…</div>;

  if (error) {
    return (
      <div style={styles.page}>
        <h2 style={{ marginTop: 0 }}>Map</h2>
        <div style={styles.errorBox}>{error}</div>
      </div>
    );
  }

  const neighborhoods = data?.neighborhoods || [];

  return (
    <div style={styles.page}>
      <h2 style={{ marginTop: 0 }}>Map (Neighborhood Intensity)</h2>
      <div style={styles.muted}>
        This is a simple “map-data” preview. Later we’ll replace with a real map
        component.
      </div>

      <div style={styles.cards}>
        {neighborhoods.map((n) => (
          <div key={n.neighborhood} style={styles.card}>
            <div style={{ fontWeight: 900 }}>{n.neighborhood}</div>
            <div style={styles.meta}>{n.article_count} articles</div>

            <div style={{ marginTop: 10, fontWeight: 800, fontSize: 13 }}>
              Theme distribution
            </div>
            <div style={styles.pillsWrap}>
              {(n.theme_distribution || []).map((t) => (
                <div key={t.id} style={styles.pill}>
                  Theme {t.id}: {t.count}
                </div>
              ))}
            </div>

            <div style={{ marginTop: 10, fontWeight: 800, fontSize: 13 }}>
              Top keywords
            </div>
            <div style={styles.pillsWrap}>
              {(n.top_keywords || []).slice(0, 10).map((k) => (
                <div key={k.keyword} style={styles.pill}>
                  {k.keyword}: {k.count}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  page: {
    maxWidth: 980,
    margin: "0 auto",
    padding: "18px 14px 60px",
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif',
    color: "#111827",
  },
  muted: { fontSize: 13, color: "#6b7280", marginBottom: 14, marginTop: 6 },
  errorBox: {
    border: "1px solid #fecaca",
    background: "#fff1f2",
    borderRadius: 12,
    padding: 12,
    marginTop: 14,
    color: "#991b1b",
  },
  cards: { display: "grid", gap: 12 },
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 14,
    background: "#fff",
  },
  meta: { fontSize: 12, color: "#6b7280", marginTop: 6 },
  pillsWrap: { display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8 },
  pill: {
    border: "1px solid #e5e7eb",
    borderRadius: 999,
    padding: "8px 10px",
    background: "#fff",
    fontSize: 12,
  },
};
