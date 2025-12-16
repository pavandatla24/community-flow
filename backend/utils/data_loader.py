# backend/utils/data_loader.py

import json
from pathlib import Path
from typing import Any, Dict, List


def get_data_file_path() -> Path:
    """
    Resolve absolute path to:
        data/cleaned/google_topics.json
    """
    project_root = Path(__file__).resolve().parents[2]
    data_file = project_root / "data" / "cleaned" / "google_topics.json"
    return data_file


def load_articles() -> List[Dict[str, Any]]:
    """
    Load processed article data from google_topics.json.
    """
    data_file = get_data_file_path()

    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected a list of objects at the root of JSON file.")

    return data

