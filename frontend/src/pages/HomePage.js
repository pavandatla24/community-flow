// frontend/src/pages/HomePage.js

import React, { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import { api } from "../services/api";

export default function HomePage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [themes, setThemes] = useState(null);
  const [report, setReport] = useState(null);
  const [clusters, setClusters] = useState(null);

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        setLoading(true);
        setError("");

        const [themesRes, reportRes, clustersRes] = await Promise.all([
          api.themes(),
          api.reportData({ limit: 5, sort: "date_desc" }),
          api.clusters(),
        ]);

        if (!mounted) return;

        setThemes(themesRes);
        setReport(reportRes);
        setClusters(clustersRes);
      } catch (e) {
        if (!mounted) return;
        setError(e.message || "Failed to load data");
      } finally {
        if (!mounted) return;
        setLoading(false);
      }
    }

    load();
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) return <div style={styles.page}>Loading…</div>;

  if (error) {
    return (
      <div style={styles.page}>
        <h2 style={{ marginTop: 0 }}>Community Flow</h2>
        <div style={styles.errorBox}>
          <div style={{ fontWeight: 700, marginBottom: 6 }}>Error</div>
          <div style={{ marginBottom: 10 }}>{error}</div>
          <div style={{ fontSize: 12, color: "#6b7280" }}>
            Make sure backend is running at{" "}
            <code>http://127.0.0.1:8000</code> and CORS is enabled.
          </div>
        </div>
      </div>
    );
  }

  const totalArticles = report?.total_articles ?? themes?.total_articles ?? 0;
  const topTheme = report?.theme_distribution?.[0];
  const topCluster = report?.top_clusters?.[0];

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div>
          <h2 style={{ margin: 0 }}>Community Flow</h2>
          <div style={styles.muted}>Weekly snapshot dashboard (Google RSS)</div>
        </div>
      </header>

      <section style={styles.grid}>
        <StatCard
          title="Total Articles"
          value={totalArticles}
          subtitle="Current weekly snapshot"
        />
        <StatCard
          title="Top Theme"
          value={topTheme ? `Theme ${topTheme.id}` : "—"}
          subtitle={topTheme ? `${topTheme.count} tagged items` : "No theme data"}
        />
        <StatCard
          title="Top Cluster"
          value={topCluster ? `Topic ${topCluster.topic_id}` : "—"}
          subtitle={topCluster ? `${topCluster.count} items` : "No cluster data"}
        />
      </section>

      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Latest Items</h3>
        <div style={styles.list}>
          {(report?.latest_items || []).map((item, idx) => (
            <a
              key={idx}
              href={item.link}
              target="_blank"
              rel="noreferrer"
              style={styles.listItem}
            >
              <div style={{ fontWeight: 700 }}>{item.title || "Untitled"}</div>
              <div style={styles.meta}>
                <span>{item.date || "No date"}</span>
                <span style={styles.dot}>•</span>
                <span>{item.source || "Unknown source"}</span>
                <span style={styles.dot}>•</span>
                <span>{item.neighborhood || "Unknown neighborhood"}</span>
              </div>
            </a>
          ))}
        </div>
      </section>

      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Top Clusters (Preview)</h3>
        <div style={styles.list}>
          {(clusters?.clusters || []).slice(0, 6).map((c) => (
            <div key={c.topic_id} style={styles.clusterCard}>
              <div style={{ fontWeight: 800 }}>Topic {c.topic_id}</div>
              <div style={styles.meta}>
                <span>{c.count} items</span>
                <span style={styles.dot}>•</span>
                <span>
                  Top keywords:{" "}
                  {(c.top_keywords || [])
                    .slice(0, 3)
                    .map((k) => k.keyword)
                    .join(", ") || "—"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section style={styles.section}>
        <h3 style={styles.sectionTitle}>Theme Distribution</h3>
        <div style={styles.pillsWrap}>
          {(themes?.themes || []).map((t) => (
            <div key={t.id} style={styles.pill}>
              Theme {t.id}: {t.count}
            </div>
          ))}
        </div>
      </section>
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
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 18,
  },
  muted: { fontSize: 13, color: "#6b7280", marginTop: 4 },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: 12,
    marginBottom: 18,
  },
  section: { marginTop: 20 },
  sectionTitle: { margin: "0 0 10px 0" },
  list: {
    display: "grid",
    gap: 10,
  },
  listItem: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 14,
    textDecoration: "none",
    color: "inherit",
    background: "#fff",
  },
  clusterCard: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 14,
    background: "#fff",
  },
  meta: { fontSize: 12, color: "#6b7280", marginTop: 6 },
  dot: { margin: "0 6px" },
  pillsWrap: { display: "flex", flexWrap: "wrap", gap: 8 },
  pill: {
    border: "1px solid #e5e7eb",
    borderRadius: 999,
    padding: "8px 10px",
    background: "#fff",
    fontSize: 12,
    color: "#111827",
  },
  errorBox: {
    border: "1px solid #fecaca",
    background: "#fff1f2",
    borderRadius: 12,
    padding: 14,
    marginTop: 14,
  },
};
