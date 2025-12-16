from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.data_loader import load_articles
from backend.routers import themes
from backend.routers import clusters
from backend.routers import map_data
from backend.routers import report_data


app = FastAPI(
    title="Community Flow Backend",
    description="API for Community Flow — Real-Time Wellness Weather Report for Chicago",
    version="0.1.0",
)

# Allow frontend to call backend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # safe for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Load google_topics.json once at startup.
    """
    app.state.articles = load_articles()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Register routers
app.include_router(themes.router)
app.include_router(clusters.router)
app.include_router(map_data.router)
app.include_router(report_data.router)

@app.get("/")
def root():
    return {"message": "Community Flow backend is running"}

@app.get("/themes")
def get_themes():
    # placeholder; will be wired to NLP pipeline later
    return {"status": "ok", "data": []}

@app.get("/clusters")
def get_clusters():
    return {"status": "ok", "data": []}

@app.get("/map-data")
def get_map_data():
    return {"status": "ok", "data": []}

@app.get("/report-data")
def get_report_data():
    return {"status": "ok", "data": []}
