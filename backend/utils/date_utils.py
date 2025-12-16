# backend/utils/date_utils.py

from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional


def parse_rss_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parses RFC 2822 / RSS style dates like:
      "Sun, 30 Nov 2025 02:19:00 GMT"
    Returns datetime or None if parsing fails.
    """
    if not date_str:
        return None
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        return None
