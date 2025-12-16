# backend/schemas.py

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------- Shared small models ----------

class ThemeCount(BaseModel):
    id: str
    count: int


class KeywordCount(BaseModel):
    keyword: str
    count: int


# ---------- Themes endpoint ----------

class ThemesResponse(BaseModel):
    total_articles: int
    themes: List[ThemeCount]


# ---------- Clusters endpoint ----------

class ClusterArticle(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    source: Optional[str] = None
    neighborhood: Optional[str] = None
    themes: List[int] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class ClusterSummary(BaseModel):
    topic_id: int
    count: int
    top_keywords: List[KeywordCount]
    theme_distribution: List[ThemeCount]
    articles: Optional[List[ClusterArticle]] = None


class ClustersResponse(BaseModel):
    total_clusters: int
    clusters: List[ClusterSummary]


class SingleClusterResponse(ClusterSummary):
    pass


# ---------- Report-data endpoint ----------

class ReportItemCompact(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    source: Optional[str] = None
    neighborhood: Optional[str] = None
    themes: List[int] = Field(default_factory=list)
    topic_id: Optional[int] = None


class ReportClusterCount(BaseModel):
    topic_id: int
    count: int


class ReportDataResponse(BaseModel):
    total_articles: int
    theme_distribution: List[ThemeCount]
    top_clusters: List[ReportClusterCount]
    latest_items: List[ReportItemCompact]
