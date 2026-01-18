// import { useEffect, useState } from "react";
// import { apiGet } from "../services/api";
// import JsonBlock from "../components/JsonBlock";

// export default function ClustersPage() {
//   const [data, setData] = useState(null);
//   const [error, setError] = useState("");

//   useEffect(() => {
//     apiGet("/clusters")
//       .then(setData)
//       .catch((e) => setError(e.message || "Failed to load"));
//   }, []);

//   return (
//     <div>
//       <h2>Clusters</h2>
//       {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
//       {data ? <JsonBlock data={data} /> : <p>Loading...</p>}
//     </div>
//   );
// }

// frontend/src/pages/ClustersPage.js

import React, { useEffect, useState } from "react";
import { api } from "../services/api";

export default function ClustersPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [clusters, setClusters] = useState([]);
  const [selected, setSelected] = useState(null); // selected cluster details

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        setLoading(true);
        setError("");
        const res = await api.clusters();
        if (!mounted) return;
        setClusters(res.clusters || []);
      } catch (e) {
        if (!mounted) return;
        setError(e.message || "Failed to load clusters");
      } finally {
        if (!mounted) return;
        setLoading(false);
      }
    }

    load();
    return () => (mounted = false);
  }, []);

  async function openCluster(topicId) {
    try {
      setError("");
      const res = await api.clusters({
        topic_id: topicId,
        include_articles: true,
        limit_articles: 5,
      });
      setSelected(res);
    } catch (e) {
      setError(e.message || "Failed to load cluster details");
    }
  }

  if (loading) return <div style={styles.page}>Loading…</div>;

  return (
    <div style={styles.page}>
      <h2 style={{ marginTop: 0 }}>Clusters</h2>
      <div style={styles.muted}>
        Click a topic to view details (uses topic_id filtering).
      </div>

      {error ? <div style={styles.errorBox}>{error}</div> : null}

      <div style={styles.grid}>
        <div style={styles.list}>
          {(clusters || []).map((c) => (
            <button
              key={c.topic_id}
              style={styles.clusterBtn}
              onClick={() => openCluster(c.topic_id)}
            >
              <div style={{ fontWeight: 800 }}>Topic {c.topic_id}</div>
              <div style={styles.meta}>
                {c.count} items •{" "}
                {(c.top_keywords || [])
                  .slice(0, 3)
                  .map((k) => k.keyword)
                  .join(", ")}
              </div>
            </button>
          ))}
        </div>

        <div style={styles.detail}>
          {!selected ? (
            <div style={styles.placeholder}>Select a topic to view details.</div>
          ) : (
            <div>
              <div style={{ fontWeight: 900, fontSize: 18 }}>
                Topic {selected.topic_id}
              </div>
              <div style={styles.meta}>{selected.count} items</div>

              <h3 style={styles.h3}>Top keywords</h3>
              <div style={styles.pillsWrap}>
                {(selected.top_keywords || []).slice(0, 10).map((k) => (
                  <div key={k.keyword} style={styles.pill}>
                    {k.keyword}: {k.count}
                  </div>
                ))}
              </div>

              <h3 style={styles.h3}>Sample articles</h3>
              <div style={styles.cards}>
                {(selected.articles || []).map((a, idx) => (
                  <a
                    key={idx}
                    href={a.link}
                    target="_blank"
                    rel="noreferrer"
                    style={styles.card}
                  >
                    <div style={{ fontWeight: 800 }}>{a.title}</div>
                    <div style={styles.meta}>
                      {a.date} • {a.source} • {a.neighborhood}
                    </div>
                  </a>
                ))}
                {(!selected.articles || selected.articles.length === 0) && (
                  <div style={styles.placeholder}>No articles returned.</div>
                )}
              </div>
            </div>
          )}
        </div>
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
    marginBottom: 14,
    color: "#991b1b",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1.2fr",
    gap: 14,
  },
  list: { display: "grid", gap: 10 },
  clusterBtn: {
    textAlign: "left",
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 14,
    background: "#fff",
    cursor: "pointer",
  },
  detail: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 14,
    background: "#fff",
    minHeight: 240,
  },
  placeholder: { color: "#6b7280", fontSize: 14 },
  meta: { fontSize: 12, color: "#6b7280", marginTop: 6 },
  h3: { margin: "14px 0 8px 0" },
  pillsWrap: { display: "flex", flexWrap: "wrap", gap: 8 },
  pill: {
    border: "1px solid #e5e7eb",
    borderRadius: 999,
    padding: "8px 10px",
    background: "#fff",
    fontSize: 12,
  },
  cards: { display: "grid", gap: 10 },
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 12,
    textDecoration: "none",
    color: "inherit",
    background: "#fff",
  },
};
