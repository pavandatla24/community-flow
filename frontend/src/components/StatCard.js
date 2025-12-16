// frontend/src/components/StatCard.js

import React from "react";

export default function StatCard({ title, value, subtitle }) {
  return (
    <div style={styles.card}>
      <div style={styles.title}>{title}</div>
      <div style={styles.value}>{value}</div>
      {subtitle ? <div style={styles.subtitle}>{subtitle}</div> : null}
    </div>
  );
}

const styles = {
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 16,
    background: "#fff",
    boxShadow: "0 1px 2px rgba(0,0,0,0.04)",
  },
  title: { fontSize: 12, color: "#6b7280", marginBottom: 8 },
  value: { fontSize: 24, fontWeight: 700, color: "#111827" },
  subtitle: { marginTop: 8, fontSize: 12, color: "#6b7280" },
};
