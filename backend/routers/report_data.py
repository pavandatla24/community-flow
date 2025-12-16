# backend/routers/report_data.py

from collections import Counter
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, HTTPException, Request

from backend.schemas import (
    ReportDataResponse,
    ThemeCount,
    ReportClusterCount,
    ReportItemCompact,
)
from backend.utils.date_utils import parse_rss_date

router = APIRouter(tags=["report-data"])


def _get_articles(request: Request) -> List[Dict[str, Any]]:
    articles = getattr(request.app.state, "articles", None)
    if articles is None:
        raise HTTPException(status_code=500, detail="Articles not loaded at startup.")
    return articles


@router.get("/report-data", response_model=ReportDataResponse)
async def get_report_data(
    request: Request,
    limit: int = 15,
    sort: Literal["none", "date_desc", "date_asc"] = "none",
) -> ReportDataResponse:
    """
    Frontend-friendly report summary.

    Query params:
      - limit: number of latest items to return (default 15)
      - sort:
          "none" (keep file order),
          "date_desc" (newest first),
          "date_asc" (oldest first)
    """
    articles = _get_articles(request)

    # optional sorting
    items = list(articles)
    if sort != "none":
        def key_fn(a: Dict[str, Any]):
            dt = parse_rss_date(a.get("date"))
            return dt if dt else parse_rss_date("Thu, 01 Jan 1970 00:00:00 GMT")

        reverse = sort == "date_desc"
        items.sort(key=key_fn, reverse=reverse)

    theme_counter = Counter()
    topic_counter = Counter()

    for a in items:
        for t in a.get("themes") or []:
            theme_counter[str(t)] += 1
        tid = a.get("topic_id")
        if tid is not None:
            topic_counter[str(tid)] += 1

    latest_items: List[ReportItemCompact] = []
    safe_limit = max(0, min(limit, 200))  # hard safety cap
    for a in items[:safe_limit]:
        latest_items.append(
            ReportItemCompact(
                title=a.get("title"),
                date=a.get("date"),
                link=a.get("link"),
                source=a.get("source"),
                neighborhood=a.get("neighborhood"),
                themes=a.get("themes") or [],
                topic_id=a.get("topic_id"),
            )
        )

    return ReportDataResponse(
        total_articles=len(items),
        theme_distribution=[ThemeCount(id=tid, count=c) for tid, c in theme_counter.most_common()],
        top_clusters=[ReportClusterCount(topic_id=int(tid), count=c) for tid, c in topic_counter.most_common(10)],
        latest_items=latest_items,
    )
