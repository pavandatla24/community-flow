# Community Flow

**A Real-Time Wellness Weather Report for Chicago**

Amobile-first web application designed for women of color leading healing, movement, and community spaces in Chicago. Community Flow scrapes public wellness content, classifies it into six community-rooted themes using NLP, generates weekly "needs clusters," visualizes neighborhood patterns, and provides downloadable weekly wellness reports.

---

## About Community Flow

Community Flow is a data-driven wellness intelligence platform that helps community leaders, organizers, and funders understand what their communities need in real time. Built specifically for women of color in Chicago who lead wellness spaces, the platform provides actionable insights grounded in actual community needs rather than assumptions.

**Core Promise:** *"See what your community needs in real time — rest, joy, healing, movement, care."*

### Design Philosophy

- **Warm, inclusive aesthetic:** Golds, deep corals, soft greens with curvy shapes and low-contrast shadows
- **No tech-bro UI:** Designed with community-first principles
- **Fully bilingual:** English/Spanish support
- **Ethical data practices:** Public-only scraping, no PII, anonymized excerpts, opt-out ready

---

## What Problem Does It Solve?

### For Community Leaders

- **Data for funders and grants:** Access to real-time data about community wellness needs to support funding applications and partnerships
- **Stay grounded in community needs:** Make decisions based on actual community signals, not assumptions
- **Identify gaps and opportunities:** See where wellness resources are needed most across Chicago neighborhoods

### For Funders & Partners

- **Evidence-based insights:** Understand community wellness trends through data-driven analysis
- **Neighborhood-level visibility:** See which areas have the most activity and where support is needed
- **Weekly snapshots:** Track changes in community needs over time

### The Challenge

Without Community Flow, community leaders rely on:
- Word-of-mouth and personal networks
- Limited visibility into city-wide wellness trends
- Difficulty quantifying community needs for grant applications
- No systematic way to track what's happening across neighborhoods

Community Flow solves this by providing a systematic, data-driven approach to understanding wellness needs across Chicago.

---

## High-Level Architecture

```
┌─────────────────┐
│   Data Sources  │
│  (Public APIs,  │
│   RSS Feeds,    │
│   Web Scraping) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Scraper Module │
│  (Module A)     │
│  • Events       │
│  • Workshops    │
│  • Blogs        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  NLP Pipeline   │
│  (Module B)     │
│  • Text Clean   │
│  • EN/ES Detect │
│  • Classify     │
│  • Topic Model  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Processed Data │
│  (JSON Files)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│
│  (Module C)     │
│  • /themes      │
│  • /clusters    │
│  • /map-data    │
│  • /report-data │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  React Frontend │
│  (Module D)     │
│  • Home Page    │
│  • Map View     │
│  • Clusters     │
│  • Reports      │
└─────────────────┘
```

---

## End-to-End Flow

1. **Scrape public wellness-related content**
   - Collect data from public event pages, workshop descriptions, and wellness blogs
   - Filter by Chicago location and wellness keywords
   - Save raw JSON data to `data/raw/`

2. **Clean and normalize text**
   - Remove HTML, normalize whitespace, handle special characters
   - Extract keywords and metadata
   - Save cleaned data to `data/clean/`

3. **Apply NLP (themes, embeddings, topics)**
   - Detect language (English/Spanish)
   - Classify content into six community-rooted themes
   - Generate topic clusters using TF-IDF and KMeans
   - Save processed data to `data/cleaned/`

4. **Save weekly processed datasets**
   - Store final processed data with themes, topics, and metadata
   - Backend loads latest dataset on startup

5. **Serve insights via FastAPI**
   - Expose REST API endpoints for themes, clusters, map data, and reports
   - Load processed data and serve to frontend

6. **Visualize results in a React frontend**
   - Mobile-first UI displaying top needs, joy themes, active neighborhoods
   - Interactive map showing neighborhood intensity
   - Clusters page with weekly topic analysis
   - Weekly report download functionality

7. **(Later) Automate weekly refresh**
   - GitHub Actions workflow to run scraper → NLP pipeline → save new weekly file
   - Backend automatically picks up latest data

---

## Themes

Community Flow classifies content into **six community-rooted themes**:

### 1. Stress Relief + Burnout Recovery
Keywords: relax, reset, renewal, mental, stress, burnout, healing, yoga, retreat

### 2. Body Love + Self-Image
Keywords: body, self, image, spa, baths, wellness

### 3. Movement Access + Beginner-Friendly
Keywords: meditation, movement, beginners, try, experiences, accessible

### 4. Cultural / Spiritual Connection
Keywords: spiritual, culture, community, mindfulness, nature, sanctuaries, healing arts

### 5. Financial Access + Mutual Aid
Keywords: free, access, affordable, low cost, mutual aid

### 6. Community Care + Solidarity
Keywords: safe spaces, community, together, group, nonprofit, support

Each piece of content can be tagged with multiple themes, allowing for nuanced understanding of community needs.

---

## Project Structure

```
community-flow/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI app entry point
│   ├── routers/         # API route handlers
│   ├── utils/           # Utility functions
│   └── requirements.txt  # Python dependencies
│
├── scraper/              # Web scraping module
│   ├── scrape_google_rss.py
│   ├── scrape_eventbrite.py
│   ├── scrape_meetup.py
│   └── run_all.py
│
├── nlp/                  # NLP processing pipeline
│   ├── topic_model.py   # Topic modeling (TF-IDF + KMeans)
│   └── process_pipeline.py
│
├── scripts/              # Data processing scripts
│   ├── clean_text.py
│   ├── label_data_google.py
│   └── clean_google_clean_json.py
│
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── components/  # Reusable components
│   │   └── services/    # API service layer
│   └── package.json
│
├── data/                 # Data storage (not committed)
│   ├── raw/             # Raw scraped data
│   ├── clean/           # Cleaned text data
│   ├── labeled/         # Theme-labeled data
│   └── cleaned/         # Final processed data
│
├── automation/           # Automation workflows
│   └── weekly_refresh.py
│
└── docs/                 # Documentation
    ├── README.md
    └── ETHICS.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Virtual environment (recommended)

### Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate     # macOS/Linux

# Install dependencies
cd backend
pip install -r requirements.txt

# Run backend server
python -m uvicorn backend.main:app --reload
```

Backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will be available at `http://localhost:3000`

### Running the Data Pipeline

```bash
# Run scrapers
python scraper/run_all.py

# Process data (in sequence)
python scripts/clean_text.py
python scripts/label_data_google.py
python nlp/topic_model.py
```

---

## API Endpoints

- `GET /health` — Health check
- `GET /themes` — Get theme distribution
- `GET /clusters` — Get topic clusters
- `GET /map-data?neighborhood={name}` — Get neighborhood data
- `GET /report-data?limit={n}&sort={order}` — Get report data

---

## Ethics & Privacy

- **Public-only scraping:** Only collects publicly available content
- **No PII:** No usernames, emails, or personal information stored
- **Anonymized excerpts:** Only text excerpts used for analysis
- **Opt-out ready:** Built with takedown request handling in mind

See `docs/ETHICS.md` for full ethical guidelines.

---

**Built with ❤️ for Chicago's wellness community**








