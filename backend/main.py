from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Community Flow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
