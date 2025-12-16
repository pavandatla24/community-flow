# backend/routers/clusters.py

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Request

from backend.schemas import (
    ClustersResponse,
    ClusterSummary,
    ThemeCount,
    KeywordCount,
    ClusterArticle,
    SingleClusterResponse,
)

router = APIRouter(tags=["clusters"])


def _get_articles(request: Request) -> List[Dict[str, Any]]:
    articles = getattr(request.app.state, "articles", None)
    if articles is None:
        raise HTTPException(status_code=500, detail="Articles not loaded at startup.")
    return articles


@router.get("/clusters", response_model=Union[ClustersResponse, SingleClusterResponse])
async def get_clusters(
    request: Request,
    topic_id: Optional[int] = None,
    include_articles: bool = False,
    limit_articles: int = 20,
) -> Union[ClustersResponse, SingleClusterResponse]:
    """
    Returns clusters grouped by topic_id.

    Query params:
      - topic_id: if provided, returns ONLY that cluster
      - include_articles: if true, includes sample articles per cluster
      - limit_articles: max articles returned per cluster when include_articles=true
    """
    articles = _get_articles(request)

    clusters: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for a in articles:
        tid = a.get("topic_id")
        if tid is None:
            continue
        clusters[str(tid)].append(a)

    # ---- Return a single cluster if topic_id is provided ----
    if topic_id is not None:
        key = str(topic_id)
        if key not in clusters:
            # consistent empty response for missing topic
            return SingleClusterResponse(
                topic_id=topic_id,
                count=0,
                top_keywords=[],
                theme_distribution=[],
                articles=[] if include_articles else None,
            )

        return _build_cluster_response(
            topic_key=key,
            cluster_articles=clusters[key],
            include_articles=include_articles,
            limit_articles=limit_articles,
            single=True,
        )

    # ---- Otherwise return all clusters ----
    out: List[ClusterSummary] = []
    for key in sorted(clusters.keys(), key=lambda x: int(x)):
        out.append(
            _build_cluster_response(
                topic_key=key,
                cluster_articles=clusters[key],
                include_articles=include_articles,
                limit_articles=limit_articles,
                single=False,
            )
        )

    return ClustersResponse(total_clusters=len(out), clusters=out)


def _build_cluster_response(
    topic_key: str,
    cluster_articles: List[Dict[str, Any]],
    include_articles: bool,
    limit_articles: int,
    single: bool,
) -> Union[ClusterSummary, SingleClusterResponse]:
    keyword_counter = Counter()
    theme_counter = Counter()

    for a in cluster_articles:
        for k in a.get("keywords") or []:
            keyword_counter[str(k).lower()] += 1
        for t in a.get("themes") or []:
            theme_counter[str(t)] += 1

    articles_out = None
    if include_articles:
        articles_out = []
        for a in cluster_articles[: max(0, limit_articles)]:
            articles_out.append(
                ClusterArticle(
                    title=a.get("title"),
                    date=a.get("date"),
                    link=a.get("link"),
                    source=a.get("source"),
                    neighborhood=a.get("neighborhood"),
                    themes=a.get("themes") or [],
                    keywords=a.get("keywords") or [],
                )
            )

    common_kwargs = dict(
        topic_id=int(topic_key),
        count=len(cluster_articles),
        top_keywords=[KeywordCount(keyword=k, count=c) for k, c in keyword_counter.most_common(10)],
        theme_distribution=[ThemeCount(id=tid, count=c) for tid, c in theme_counter.most_common()],
        articles=articles_out,
    )

    if single:
        return SingleClusterResponse(**common_kwargs)
    return ClusterSummary(**common_kwargs)
