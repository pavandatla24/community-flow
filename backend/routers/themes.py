# backend/routers/themes.py

from fastapi import APIRouter, Request, HTTPException
from collections import Counter
from typing import Any, Dict, List

from backend.schemas import ThemesResponse, ThemeCount

router = APIRouter(tags=["themes"])


def _get_articles(request: Request) -> List[Dict[str, Any]]:
    articles = getattr(request.app.state, "articles", None)
    if articles is None:
        raise HTTPException(status_code=500, detail="Articles not loaded at startup.")
    return articles


@router.get("/themes", response_model=ThemesResponse)
async def get_themes(request: Request) -> ThemesResponse:
    articles = _get_articles(request)

    theme_counts = Counter()

    for article in articles:
        themes = article.get("themes") or []
        if isinstance(themes, list):
            for t in themes:
                theme_counts[str(t)] += 1
        else:
            theme_counts[str(themes)] += 1

    return ThemesResponse(
        total_articles=len(articles),
        themes=[ThemeCount(id=tid, count=theme_counts[tid]) for tid in sorted(theme_counts.keys())],
    )
