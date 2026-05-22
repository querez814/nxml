"""Alpha Vantage NEWS_SENTIMENT fetch helper (shared URL building + pacing via av_get_json_async)."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import dotenv as env
from fastapi import HTTPException

from fetch.av_util import av_get_json_async

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

# Default broad topics for GET /news/sentiment/market when caller omits `topics`.
# Alpha Vantage topic slugs (comma-separated), e.g. economy_fiscal, financial_markets, technology.
AV_NEWS_MARKET_TOPICS = os.getenv(
    "AV_NEWS_MARKET_TOPICS",
    "economy_fiscal,financial_markets,technology",
)
# Optional comma-separated tickers to blend with topic filters (e.g. SPY,QQQ); empty = topics only.
AV_NEWS_MARKET_TICKERS = os.getenv("AV_NEWS_MARKET_TICKERS", "").strip()


async def fetch_news_sentiment_async(
    *,
    tickers: Optional[str] = None,
    topics: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Call Alpha Vantage NEWS_SENTIMENT. Raises HTTPException on throttle (via av_get_json_async)."""
    if not av_api:
        raise HTTPException(status_code=503, detail="ALPHA_VANTAGE not configured")

    params: Dict[str, Any] = {"function": "NEWS_SENTIMENT", "apikey": av_api}
    if tickers:
        params["tickers"] = tickers
    if topics:
        params["topics"] = topics
    if time_from:
        params["time_from"] = time_from
    if time_to:
        params["time_to"] = time_to
    if sort:
        params["sort"] = sort
    if limit is not None:
        params["limit"] = limit

    query = urlencode(params)
    url = f"https://www.alphavantage.co/query?{query}"
    return dict(await av_get_json_async(url))
