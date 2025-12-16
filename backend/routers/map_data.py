# backend/routers/map_data.py

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request

router = APIRouter(tags=["map-data"])


def _get_articles(request: Request) -> List[Dict[str, Any]]:
    articles = getattr(request.app.state, "articles", None)
    if articles is None:
        raise HTTPException(status_code=500, detail="Articles not loaded at startup.")
    return articles


@router.get("/map-data")
async def get_map_data(
    request: Request,
    neighborhood: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Aggregates articles by neighborhood and returns theme counts per neighborhood.

    Query params:
      - neighborhood: if provided, returns only that neighborhood's stats
    """
    articles = _get_articles(request)

    # Normalize neighborhood names
    def norm(n: Any) -> str:
        if not n:
            return "Unknown"
        return str(n).strip()

    by_neighborhood: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for a in articles:
        by_neighborhood[norm(a.get("neighborhood"))].append(a)

    if neighborhood is not None:
        key = norm(neighborhood)
        return _build_neighborhood_block(key, by_neighborhood.get(key, []))

    out = []
    for key in sorted(by_neighborhood.keys()):
        out.append(_build_neighborhood_block(key, by_neighborhood[key]))

    return {"total_neighborhoods": len(out), "neighborhoods": out}


def _build_neighborhood_block(name: str, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    theme_counter = Counter()
    keyword_counter = Counter()

    for a in articles:
        for t in a.get("themes") or []:
            theme_counter[str(t)] += 1
        for k in a.get("keywords") or []:
            keyword_counter[str(k).lower()] += 1

    return {
        "neighborhood": name,
        "article_count": len(articles),
        "theme_distribution": [{"id": tid, "count": c} for tid, c in theme_counter.most_common()],
        "top_keywords": [{"keyword": k, "count": c} for k, c in keyword_counter.most_common(10)],
    }
