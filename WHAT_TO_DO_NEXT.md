# Community Flow — What’s Done & What To Do Next

This document summarizes the current state of the project and the remaining work for the next developer or team. Use it together with **README.md** and **flow.md** (same folder) for full context.

---

## Where the Project Stands (What’s Done)

### Backend (Module C) — Complete
- FastAPI app with CORS, startup data load from `data/cleaned/google_topics.json`
- Endpoints: `/health`, `/themes`, `/clusters`, `/map-data`, `/report-data`, `/report-pdf`
- Data loader, report builder, and PDF service (reportlab) for weekly report download
- All endpoints read from in-memory articles loaded at startup

### Data Pipeline (Modules A & B) — Complete
- **Scraper:** `scraper/scrape_google_rss.py` — fetches Google News RSS, saves to `data/raw/`
- **Cleaning:** `scripts/clean_text.py`, `scripts/clean_google_clean_json.py` — output to `data/clean/`
- **Themes:** `scripts/label_data_google.py` — assigns 6 themes, output to `data/labeled/`
- **Topics:** `nlp/topic_model.py` — TF-IDF + KMeans, output to `data/cleaned/google_topics.json`
- Pipeline is run manually; data is currently **static** (one snapshot) for development/demo

### Frontend (Module D) — Mostly Complete
- React app with API service (`frontend/src/services/api.js`) calling all backend endpoints
- Pages: Home, Themes, Clusters, Report, Map (structure exists)
- Home page shows theme distribution, clusters, latest items, stats
- Report page supports report data and PDF download
- **Map view:** Backend `/map-data` is ready; frontend Map page still needs **integration** (e.g. map library, neighborhood visualization) to be fully complete

### PDF Report (Module E) — Complete
- Weekly report PDF generated from `build_report_data()` + `pdf_service`
- Downloaded via `GET /report-pdf`

### Documentation — In Place
- **README.md** — Project overview, architecture, getting started, API list, themes
- **flow.md** — Full system flow: scraping → cleaning → labeling → topic model → backend → frontend; includes “Simple Step-by-Step Flow” runbook
- **docs/ETHICS.md** — Ethical guidelines for data use
- **WHAT_TO_DO_NEXT.md** — This file (root)

---

## What Needs To Be Done Next (In Order)

### 1. Map View Integration (Frontend)
- **Goal:** Complete the Map page so it shows neighborhood-level wellness data.
- **Backend:** Already done — `GET /map-data` returns neighborhoods with article counts, theme distribution, top keywords.
- **Frontend:** Integrate a map (e.g. Leaflet, Mapbox, or similar) in `frontend/src/pages/MapPage.js`, fetch `api.mapData()`, and display neighborhoods/intensity (e.g. markers or choropleth). Optional: filter by neighborhood via query param.
- **Outcome:** UI portion of the system is fully complete.

### 2. Weekly Data Refresh (Move Off Static Data)
- **Goal:** Stop relying on a single static `google_topics.json`; refresh data regularly.
- **Current:** Data is produced by manually running the pipeline (scraper → clean → keywords → themes → topics). Backend loads whatever is in `data/cleaned/google_topics.json` at startup.
- **Next steps:**
  - Run the full pipeline on a schedule (e.g. weekly) so `data/cleaned/google_topics.json` is updated.
  - Ensure the backend uses the latest file (already does if it restarts after the pipeline runs, or add a reload mechanism if needed).
- **Outcome:** “Real-time” wellness report reflects up-to-date data.

### 3. Automate Pipeline (Module F)
- **Goal:** No manual runs; pipeline runs automatically (e.g. weekly).
- **Options:** GitHub Actions workflow, or a script in `automation/` triggered by a scheduler (e.g. cron, cloud scheduler).
- **Steps:** Run in sequence: scraper → `clean_text.py` → `clean_google_clean_json.py` → `label_data_google.py` → `topic_model.py`; output to `data/cleaned/google_topics.json`. If backend is deployed, ensure it picks up the new file (restart or reload).
- **Outcome:** Data is updated every week without manual intervention.

### 4. Testing
- **Goal:** Add tests so changes don’t break the system.
- **Suggestions:**
  - Backend: unit/integration tests for key endpoints (`/themes`, `/clusters`, `/map-data`, `/report-data`, `/report-pdf`) and for `report_builder` / `data_loader`.
  - Frontend: component or integration tests for main pages and API service.
  - Pipeline: smoke test that the full pipeline (scraper → topic_model) runs and produces valid `google_topics.json`.
- **Outcome:** Safer refactors and deployments.

### 5. Deploy (Module G)
- **Goal:** Run the app in production.
- **Typical setup:**
  - **Backend:** Deploy FastAPI (e.g. Render, Railway, Fly.io). Set env if needed; ensure `data/cleaned/google_topics.json` is available (e.g. from automation or a mounted volume).
  - **Frontend:** Deploy React (e.g. Vercel, Netlify). Set `REACT_APP_API_BASE_URL` to the deployed backend URL.
  - **Automation:** If using GitHub Actions, run from repo; ensure artifact or storage is wired so the deployed backend can load the latest file.
- **Outcome:** Live “Real-Time Wellness Weather Report” for Chicago.

---

## Quick Reference

| Item | Status | Next action |
|------|--------|-------------|
| Map view (frontend) | Pending integration | Add map library, wire `/map-data`, show neighborhoods |
| Data freshness | Static snapshot | Run pipeline weekly; then automate (Module F) |
| Automation (Module F) | Not implemented | Add scheduled job (e.g. GitHub Action) to run full pipeline |
| Testing | Not implemented | Add backend, frontend, and pipeline tests |
| Deployment (Module G) | Not implemented | Deploy backend + frontend; connect automation to deployed backend |

---

## Where to Look in the Repo

- **Architecture & flow:** `flow.md` (root)
- **Setup & API overview:** `README.md` (root)
- **Backend entry:** `backend/main.py`
- **Data pipeline:** `scraper/`, `scripts/`, `nlp/topic_model.py`
- **Frontend pages:** `frontend/src/pages/` (HomePage, MapPage, ClustersPage, ReportPage, ThemesPage)
- **API service:** `frontend/src/services/api.js`
