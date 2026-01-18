// frontend/src/services/api.js

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

async function get(path, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const url = `${API_BASE_URL}${path}${qs ? `?${qs}` : ""}`;

  const res = await fetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`GET ${url} failed: ${res.status} ${text}`);
  }
  return res.json();
}

export const api = {
  health: () => get("/health"),
  themes: () => get("/themes"),
  clusters: (params) => get("/clusters", params || {}),
  mapData: (params) => get("/map-data", params || {}),
  reportData: (params) => get("/report-data", params || {}),
};
