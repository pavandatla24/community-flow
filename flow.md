# Community Flow - Complete Data Flow Documentation

## Overview

This document explains the complete end-to-end data flow in Community Flow, from scraping raw wellness content to displaying insights in the frontend.

**Key Point:** The frontend calls APIs which fetch data from `data/cleaned/google_topics.json` (loaded into memory at backend startup).

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION & PROCESSING                  │
└─────────────────────────────────────────────────────────────────┘

STEP 1: SCRAPING
   scraper/scrape_google_rss.py
   ↓ Fetches Google News RSS for Chicago wellness content
   ↓ Extracts: title, text, date, link, source, neighborhood
   ↓ Saves: data/raw/google_rss_2025-12-04.json

STEP 2: TEXT CLEANING
   scripts/clean_text.py
   ↓ Removes HTML tags, normalizes whitespace
   ↓ Reads: data/raw/google_rss_2025-12-04.json
   ↓ Saves: data/clean/google_clean.json

STEP 3: KEYWORD EXTRACTION
   scripts/clean_google_clean_json.py
   ↓ Extracts keywords from cleaned text
   ↓ Adds: clean_text, keywords fields
   ↓ Saves: data/clean/google_step2.json

STEP 4: THEME LABELING
   scripts/label_data_google.py
   ↓ Assigns themes (1-6) based on keywords
   ↓ Adds: themes: [1, 4] to each item
   ↓ Saves: data/labeled/google_labeled.json

STEP 5: TOPIC MODELING
   nlp/topic_model.py
   ↓ Vectorizes text (TF-IDF)
   ↓ Clusters into 6 topics (KMeans)
   ↓ Adds: topic_id: 0-5 to each item
   ↓ Saves: data/cleaned/google_topics.json ← FINAL PROCESSED DATA

┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API LAYER                          │
└─────────────────────────────────────────────────────────────────┘

STEP 6: BACKEND STARTUP
   backend/main.py → @app.on_event("startup")
   ↓ Calls: backend/utils/data_loader.py → load_articles()
   ↓ Reads: data/cleaned/google_topics.json
   ↓ Stores in memory: app.state.articles = [all articles]

STEP 7: API ENDPOINTS
   All routers read from app.state.articles:
   
   • backend/routers/themes.py → GET /themes
     - Counts theme occurrences
     - Returns: {total_articles, themes: [{id, count}]}
   
   • backend/routers/clusters.py → GET /clusters
     - Groups articles by topic_id
     - Returns: {total_clusters, clusters: [{topic_id, count, top_keywords}]}
   
   • backend/routers/report_data.py → GET /report-data
     - Aggregates themes, topics, latest items
     - Returns: {total_articles, theme_distribution, top_clusters, latest_items}
   
   • backend/routers/map_data.py → GET /map-data
     - Groups by neighborhood
     - Returns: {total_neighborhoods, neighborhoods: [{neighborhood, article_count, theme_distribution}]}

┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND DISPLAY                          │
└─────────────────────────────────────────────────────────────────┘

STEP 8: FRONTEND API CALLS
   frontend/src/services/api.js
   ↓ Makes HTTP requests to backend endpoints
   ↓ api.themes() → GET http://127.0.0.1:8000/themes
   ↓ api.clusters() → GET http://127.0.0.1:8000/clusters
   ↓ api.reportData() → GET http://127.0.0.1:8000/report-data

STEP 9: UI RENDERING
   frontend/src/pages/HomePage.js
   ↓ Receives JSON responses from APIs
   ↓ Updates React state
   ↓ Displays: theme distribution, clusters, latest items, stats
```

---

## Detailed Step-by-Step Flow

### STEP 1: Data Scraping

**File:** `scraper/scrape_google_rss.py`

**What it does:**
- Fetches Google News RSS feed for Chicago wellness content
- Parses XML to extract article information
- Extracts: `title`, `text` (description), `date`, `link`, `source`, `neighborhood`

**Output:** `data/raw/google_rss_2025-12-04.json`

**Example structure:**
```json
{
  "title": "A 'mindful' Chicago market spotlights wellness...",
  "text": "A 'mindful' Chicago market...",
  "date": "Sun, 30 Nov 2025 02:19:00 GMT",
  "link": "https://news.google.com/rss/articles/...",
  "source": "Google News RSS",
  "neighborhood": "Chicago"
}
```

---

### STEP 2: Text Cleaning

**File:** `scripts/clean_text.py`

**What it does:**
- Removes HTML tags using regex
- Converts HTML entities (`&nbsp;` → spaces)
- Normalizes whitespace
- Strips leading/trailing whitespace

**Input:** `data/raw/google_rss_2025-12-04.json`  
**Output:** `data/clean/google_clean.json`

**Transformation:**
- Before: `"<p>A 'mindful' Chicago market&nbsp;spotlights wellness</p>"`
- After: `"A 'mindful' Chicago market spotlights wellness"`

---

### STEP 3: Keyword Extraction

**File:** `scripts/clean_google_clean_json.py`

**What it does:**
- Extracts keywords from cleaned text
- Creates `clean_text` field (normalized text)
- Creates `keywords` array (extracted terms)

**Input:** `data/clean/google_clean.json`  
**Output:** `data/clean/google_step2.json`

**Added fields:**
```json
{
  "clean_text": "a mindful chicago market spotlights wellness...",
  "keywords": ["chicago", "mindful", "market", "spotlights", "wellness"]
}
```

---

### STEP 4: Theme Labeling

**File:** `scripts/label_data_google.py`

**What it does:**
- Analyzes `clean_text` for keyword matches
- Assigns one or more themes (1-6) to each article
- Uses keyword-based rules for classification

**Input:** `data/clean/google_step2.json`  
**Output:** `data/labeled/google_labeled.json`

**Theme Classification Rules:**

1. **Theme 1: Stress Relief + Burnout Recovery**
   - Keywords: `relax`, `reset`, `renewal`, `mental`, `stress`, `burnout`, `healing`, `yoga`, `retreat`

2. **Theme 2: Body Love + Self-Image**
   - Keywords: `body`, `self`, `image`, `muffins`, `baths`, `spa`

3. **Theme 3: Movement Access + Beginner-Friendly**
   - Keywords: `meditation`, `movement`, `beginners`, `try`, `experiences`

4. **Theme 4: Cultural / Spiritual Connection**
   - Keywords: `spiritual`, `culture`, `community`, `mindfulness`, `nature`, `sanctuaries`, `healing arts`

5. **Theme 5: Financial Access + Mutual Aid**
   - Keywords: `free`, `access`, `affordable`, `low cost`

6. **Theme 6: Community Care + Solidarity**
   - Keywords: `safe spaces`, `community`, `together`, `group`, `nonprofit`, `support`

**Added field:**
```json
{
  "themes": [1, 4]  // Can have multiple themes
}
```

---

### STEP 5: Topic Modeling

**File:** `nlp/topic_model.py`

**What it does:**
- Loads labeled data
- Vectorizes text using TF-IDF (Term Frequency-Inverse Document Frequency)
- Applies KMeans clustering to group articles into 6 topics
- Assigns `topic_id` (0-5) to each article

**Input:** `data/labeled/google_labeled.json`  
**Output:** `data/cleaned/google_topics.json` ← **FINAL PROCESSED DATA**

**Process:**
1. Extract `clean_text` from all articles
2. Create TF-IDF matrix (removes stop words, min_df=2)
3. Run KMeans with n_clusters=6
4. Assign `topic_id` to each article based on cluster

**Added field:**
```json
{
  "topic_id": 2  // 0-5, represents which topic cluster the article belongs to
}
```

**Final data structure:**
```json
{
  "title": "...",
  "text": "...",
  "clean_text": "...",
  "keywords": ["chicago", "wellness", ...],
  "themes": [1, 4],
  "topic_id": 2,
  "date": "...",
  "link": "...",
  "source": "Google News RSS",
  "neighborhood": "Chicago"
}
```

---

### STEP 6: Backend Data Loading

**File:** `backend/main.py` (startup event)  
**Utility:** `backend/utils/data_loader.py`

**What it does:**
- When FastAPI server starts, `@app.on_event("startup")` runs
- Calls `load_articles()` which:
  1. Resolves path to `data/cleaned/google_topics.json`
  2. Reads JSON file
  3. Validates it's a list
  4. Returns list of all articles
- Stores in `app.state.articles` (available to all routes)

**Code:**
```python
@app.on_event("startup")
async def startup_event():
    app.state.articles = load_articles()  # Loads all processed articles
```

**Result:** All articles are now in memory, accessible via `request.app.state.articles` in any route handler.

---

### STEP 7: API Endpoints

All API endpoints read from `app.state.articles` (loaded from `data/cleaned/google_topics.json`).

#### 7.1 Themes Endpoint

**File:** `backend/routers/themes.py`  
**Endpoint:** `GET /themes`

**What it does:**
1. Gets all articles from `app.state.articles`
2. Counts occurrences of each theme (1-6)
3. Returns theme distribution

**Response:**
```json
{
  "total_articles": 50,
  "themes": [
    {"id": "1", "count": 25},
    {"id": "2", "count": 10},
    {"id": "4", "count": 15}
  ]
}
```

#### 7.2 Clusters Endpoint

**File:** `backend/routers/clusters.py`  
**Endpoint:** `GET /clusters`

**What it does:**
1. Groups articles by `topic_id` (0-5)
2. Counts keywords per cluster
3. Counts themes per cluster
4. Returns cluster summaries with top keywords

**Response:**
```json
{
  "total_clusters": 6,
  "clusters": [
    {
      "topic_id": 0,
      "count": 12,
      "top_keywords": [
        {"keyword": "wellness", "count": 8},
        {"keyword": "chicago", "count": 6}
      ],
      "theme_distribution": [
        {"id": "1", "count": 8},
        {"id": "4", "count": 4}
      ]
    }
  ]
}
```

#### 7.3 Report Data Endpoint

**File:** `backend/routers/report_data.py`  
**Endpoint:** `GET /report-data?limit=15&sort=date_desc`

**What it does:**
1. Aggregates theme distribution across all articles
2. Counts articles per topic (top clusters)
3. Returns latest items (sorted by date)
4. Supports sorting: `none`, `date_desc`, `date_asc`

**Response:**
```json
{
  "total_articles": 50,
  "theme_distribution": [
    {"id": "1", "count": 25},
    {"id": "4", "count": 15}
  ],
  "top_clusters": [
    {"topic_id": 0, "count": 12},
    {"topic_id": 2, "count": 10}
  ],
  "latest_items": [
    {
      "title": "...",
      "date": "...",
      "link": "...",
      "source": "...",
      "neighborhood": "...",
      "themes": [1, 4],
      "topic_id": 2
    }
  ]
}
```

#### 7.4 Map Data Endpoint

**File:** `backend/routers/map_data.py`  
**Endpoint:** `GET /map-data?neighborhood=Chicago`

**What it does:**
1. Groups articles by `neighborhood`
2. Counts themes per neighborhood
3. Extracts top keywords per neighborhood
4. Returns neighborhood-level statistics

**Response:**
```json
{
  "total_neighborhoods": 5,
  "neighborhoods": [
    {
      "neighborhood": "Chicago",
      "article_count": 30,
      "theme_distribution": [
        {"id": "1", "count": 15},
        {"id": "4", "count": 10}
      ],
      "top_keywords": [
        {"keyword": "wellness", "count": 12},
        {"keyword": "chicago", "count": 10}
      ]
    }
  ]
}
```

---

### STEP 8: Frontend API Calls

**File:** `frontend/src/services/api.js`

**What it does:**
- Defines base URL: `http://127.0.0.1:8000` (or from env variable)
- Provides API methods:
  - `api.themes()` → `GET /themes`
  - `api.clusters()` → `GET /clusters`
  - `api.reportData({limit, sort})` → `GET /report-data`
  - `api.mapData(neighborhood)` → `GET /map-data`

**Code:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

export async function apiGet(path) {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  async themes() {
    return apiGet("/themes");
  },
  async clusters() {
    return apiGet("/clusters");
  },
  // ... other methods
};
```

---

### STEP 9: Frontend Display

**File:** `frontend/src/pages/HomePage.js`

**What it does:**
1. On component mount, `useEffect` runs
2. Calls multiple APIs in parallel:
   ```javascript
   const [themesRes, reportRes, clustersRes] = await Promise.all([
     api.themes(),
     api.reportData({ limit: 5, sort: "date_desc" }),
     api.clusters(),
   ]);
   ```
3. Updates React state with responses
4. Renders UI components:
   - Stat cards (total articles, top theme, top cluster)
   - Latest items list
   - Top clusters preview
   - Theme distribution pills

**Data Flow:**
```
User visits page
  ↓
useEffect triggers
  ↓
Calls api.themes(), api.reportData(), api.clusters()
  ↓
HTTP requests to backend
  ↓
Backend reads app.state.articles (from google_topics.json)
  ↓
Returns JSON responses
  ↓
Frontend updates state
  ↓
UI renders with data
```

---

## Key Points

### 1. **Single Source of Truth**
- All processed data is stored in `data/cleaned/google_topics.json`
- Backend loads this file once at startup into `app.state.articles`
- All API endpoints read from this in-memory data

### 2. **Data Transformation Pipeline**
```
Raw → Clean → Labeled → Processed
  ↓      ↓        ↓          ↓
raw/  clean/  labeled/  cleaned/
```

### 3. **No Database**
- Data is stored as JSON files
- Backend loads JSON into memory for fast access
- No database queries needed

### 4. **API-First Architecture**
- Frontend is completely decoupled from data processing
- Frontend only knows about API endpoints
- Backend handles all data aggregation and formatting

### 5. **Stateless API (with in-memory state)**
- API endpoints are stateless (no session)
- Data is loaded once at startup
- All requests read from the same in-memory dataset

---

## File Locations Summary

| Step | File | Input | Output |
|------|------|-------|--------|
| 1. Scraping | `scraper/scrape_google_rss.py` | Google RSS | `data/raw/google_rss_*.json` |
| 2. Cleaning | `scripts/clean_text.py` | `data/raw/` | `data/clean/google_clean.json` |
| 3. Keywords | `scripts/clean_google_clean_json.py` | `data/clean/` | `data/clean/google_step2.json` |
| 4. Themes | `scripts/label_data_google.py` | `data/clean/` | `data/labeled/google_labeled.json` |
| 5. Topics | `nlp/topic_model.py` | `data/labeled/` | `data/cleaned/google_topics.json` |
| 6. Load | `backend/utils/data_loader.py` | `data/cleaned/` | `app.state.articles` (memory) |
| 7. API | `backend/routers/*.py` | `app.state.articles` | JSON responses |
| 8. Fetch | `frontend/src/services/api.js` | Backend APIs | JavaScript objects |
| 9. Display | `frontend/src/pages/HomePage.js` | API responses | React UI |

---

## Answer to Your Question

**Q: Front calls APIs which fetches data from cleaned/google_topics.json, right?**

**A: Yes, exactly!**

1. Backend loads `data/cleaned/google_topics.json` into memory at startup (`app.state.articles`)
2. Frontend calls API endpoints (`/themes`, `/clusters`, `/report-data`, `/map-data`)
3. API endpoints read from `app.state.articles` (which came from `google_topics.json`)
4. Frontend receives JSON responses and displays them

So the flow is:
```
google_topics.json → app.state.articles (memory) → API endpoints → Frontend
```

