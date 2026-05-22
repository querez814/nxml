"""Routes: GET /news/sentiment/market and GET /news/sentiment/{ticker} (Alpha Vantage NEWS_SENTIMENT)."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from fetch.news_sentiment import (
    AV_NEWS_MARKET_TICKERS,
    AV_NEWS_MARKET_TOPICS,
    fetch_news_sentiment_async,
)
from fetch.summary import curate_market_news, curate_news

router = APIRouter()


@router.get("/sentiment/market")
async def sentiment_market(
    topics: Optional[str] = None,
    tickers: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = 50,
    sort_by: str = "recent",
    min_ticker_relevance: float = 0.0,
    excluded_sources: str = "Motley Fool",
):
    """
    Broad market news using NEWS_SENTIMENT. Defaults: ``AV_NEWS_MARKET_TOPICS`` and optional
    ``AV_NEWS_MARKET_TICKERS`` env when query params are omitted.
    """
    t = (tickers or "").strip() or (AV_NEWS_MARKET_TICKERS or None)
    top = (topics or "").strip() or AV_NEWS_MARKET_TOPICS
    data_json = await fetch_news_sentiment_async(
        tickers=t,
        topics=top,
        time_from=time_from,
        time_to=time_to,
        sort=sort,
        limit=limit,
    )
    excluded_list = [s.strip() for s in excluded_sources.split(",") if s.strip()]
    return curate_market_news(
        data_json,
        sort_by=sort_by,
        min_ticker_relevance=min_ticker_relevance,
        excluded_sources=excluded_list or None,
    )


@router.get("/sentiment/{ticker}")
async def sentiment_ticker(
    ticker: str,
    topics: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = 50,
    sort_by: str = "recent",
    min_relevance: float = 0.3,
    excluded_sources: str = "Motley Fool",
):
    """Ticker-scoped curated news (same shape as ``/financials/news/{ticker}`` core payload)."""
    sym = (ticker or "").strip().upper()
    if not sym or len(sym) > 8 or not sym.replace(".", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid ticker")
    if sym == "MARKET":
        raise HTTPException(
            status_code=400,
            detail="Reserved; use /news/sentiment/market",
        )

    data_json = await fetch_news_sentiment_async(
        tickers=sym,
        topics=topics,
        time_from=time_from,
        time_to=time_to,
        sort=sort,
        limit=limit,
    )
    excluded_list = [s.strip() for s in excluded_sources.split(",") if s.strip()]
    return curate_news(
        data_json,
        sym,
        sort_by,
        min_relevance,
        excluded_list or ["Motley Fool"],
    )
