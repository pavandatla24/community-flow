// import { useEffect, useState } from "react";
// import { apiGet } from "../services/api";
// import JsonBlock from "../components/JsonBlock";

// export default function ReportPage() {
//   const [data, setData] = useState(null);
//   const [error, setError] = useState("");

//   useEffect(() => {
//     apiGet("/report-data")
//       .then(setData)
//       .catch((e) => setError(e.message || "Failed to load"));
//   }, []);

//   return (
//     <div>
//       <h2>Report Data</h2>
//       {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
//       {data ? <JsonBlock data={data} /> : <p>Loading...</p>}
//     </div>
//   );
// }

// frontend/src/pages/ReportPage.js

import React, { useEffect, useState } from "react";
import { api } from "../services/api";

export default function ReportPage() {
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState(null);

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        setLoading(true);
        setError("");
        const res = await api.reportData({ limit: 10, sort: "date_desc" });
        if (!mounted) return;
        setReport(res);
      } catch (e) {
        if (!mounted) return;
        setError(e.message || "Failed to load report data");
      } finally {
        if (!mounted) return;
        setLoading(false);
      }
    }

    load();
    return () => (mounted = false);
  }, []);

  // ✅ REAL PDF DOWNLOAD
  const handleDownloadPDF = async () => {
    try {
      setDownloading(true);
      const blob = await api.reportPdf(); // calls /report-pdf

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "community_flow_weekly_report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
      alert(e.message || "PDF download failed");
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return <div style={styles.page}>Loading…</div>;

  if (error) {
    return (
      <div style={styles.page}>
        <h2 style={{ marginTop: 0 }}>Weekly Report</h2>
        <div style={styles.errorBox}>{error}</div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <h2 style={{ marginTop: 0 }}>Weekly Report</h2>
      <div style={styles.muted}>
        This page uses <code>/report-data</code>. PDF is generated from{" "}
        <code>/report-pdf</code>.
      </div>

      <div style={styles.card}>
        <div style={{ fontWeight: 900 }}>Snapshot Summary</div>
        <div style={styles.meta}>
          Total articles: <b>{report?.total_articles ?? 0}</b>
        </div>

        <h3 style={styles.h3}>Top themes</h3>
        <div style={styles.pillsWrap}>
          {(report?.theme_distribution || []).map((t) => (
            <div key={t.id} style={styles.pill}>
              Theme {t.id}: {t.count}
            </div>
          ))}
        </div>

        <h3 style={styles.h3}>Top clusters</h3>
        <div style={styles.pillsWrap}>
          {(report?.top_clusters || []).map((c) => (
            <div key={c.topic_id} style={styles.pill}>
              Topic {c.topic_id}: {c.count}
            </div>
          ))}
        </div>

        <div style={{ marginTop: 16 }}>
          <button
            style={{
              ...styles.button,
              opacity: downloading ? 0.7 : 1,
              cursor: downloading ? "not-allowed" : "pointer",
            }}
            onClick={handleDownloadPDF}
            disabled={downloading}
          >
            {downloading ? "Downloading PDF…" : "Download Weekly Report (PDF)"}
          </button>
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
    marginTop: 14,
    color: "#991b1b",
  },
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 14,
    background: "#fff",
  },
  meta: { fontSize: 12, color: "#6b7280", marginTop: 6 },
  h3: { margin: "14px 0 8px 0" },
  pillsWrap: { display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8 },
  pill: {
    border: "1px solid #e5e7eb",
    borderRadius: 999,
    padding: "8px 10px",
    background: "#fff",
    fontSize: 12,
  },
  button: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: "12px 14px",
    background: "#111827",
    color: "#fff",
    fontWeight: 800,
  },
};
