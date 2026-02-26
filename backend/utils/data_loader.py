"""
backend/utils/data_loader.py

Utility helpers for loading the processed article snapshot that backs all
analytics endpoints (/themes, /clusters, /map-data, /report-data, /report-pdf).
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def get_data_file_path() -> Path:
    """
    Resolve absolute path to:
        data/cleaned/google_topics.json

    We go two levels up from this file:
        backend/utils/data_loader.py -> backend/ -> project root.
    """
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "data" / "cleaned" / "google_topics.json"


def load_articles() -> List[Dict[str, Any]]:
    """
    Load processed article data from google_topics.json.

    This is called once at FastAPI startup (see backend/main.py) and also
    by pure helper utilities like report_builder.
    """
    data_file = get_data_file_path()

    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(
            "Expected a list of article objects at the root of the JSON file."
        )

    return data

