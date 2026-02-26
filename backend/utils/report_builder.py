# backend/utils/report_builder.py

from typing import Any, Dict, List, Optional
from collections import Counter

from .data_loader import load_articles


def build_report_data(limit: int = 10, sort: str = "date_desc") -> Dict[str, Any]:
    """
    Pure function that returns the same payload as /report-data.
    No FastAPI Request object needed.
    """
    items: List[Dict[str, Any]] = load_articles()  # list of articles from snapshot

    # --- sort ---
    # Assuming item["date"] is a comparable string; if you already parse dates, reuse your existing logic
    if sort == "date_desc":
        items_sorted = sorted(items, key=lambda x: x.get("date", ""), reverse=True)
    elif sort == "date_asc":
        items_sorted = sorted(items, key=lambda x: x.get("date", ""))
    else:
        items_sorted = items

    latest_items = items_sorted[: int(limit)]

    # --- theme distribution ---
    theme_counter = Counter()
    for it in items:
        themes = it.get("themes") or []
        for t in themes:
            theme_counter[int(t)] += 1

    theme_distribution = [{"id": k, "count": v} for k, v in sorted(theme_counter.items())]

    # --- top clusters ---
    cluster_counter = Counter()
    for it in items:
        topic_id = it.get("topic_id")
        if topic_id is not None:
            cluster_counter[int(topic_id)] += 1

    top_clusters = [
        {"topic_id": k, "count": v}
        for k, v in cluster_counter.most_common(10)
    ]

    return {
        "total_articles": len(items),
        "theme_distribution": theme_distribution,
        "top_clusters": top_clusters,
        "latest_items": latest_items,
    }
