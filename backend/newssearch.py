import asyncio
import os
from typing import Any, Dict, List

import dotenv as env
from fastapi import APIRouter

import http_client
from fetch.valuations import get_valuation_async

env.load_dotenv()
news_api = os.getenv("STOCK_NEWS_API_KEY")
router = APIRouter()


@router.get("/general")
async def general_news():
    client = http_client.get_http_client()
    market_news_url = (
        "https://stocknewsapi.com/api/v1/category"
        f"?section=general&items=8&page=1&token={news_api}"
    )
    response = await client.get(market_news_url)
    response.raise_for_status()
    response_native = response.json()
    return response_native["data"]


@router.get("/{ticker}")
async def get_ticker_news(ticker: str):
    client = http_client.get_http_client()
    news_url = (
        "https://stocknewsapi.com/api/v1"
        f"?tickers={ticker}&items=10&page=1&token={news_api}"
    )
    analyst_rate_url = (
        "https://stocknewsapi.com/api/v1/ratings"
        f"?tickers={ticker}&items=10&page=1&token={news_api}"
    )

    async def _news() -> List[Dict[str, Any]]:
        resp = await client.get(news_url)
        resp.raise_for_status()
        return resp.json()["data"]

    async def _ratings() -> List[Dict[str, Any]]:
        resp = await client.get(analyst_rate_url)
        resp.raise_for_status()
        return resp.json()["data"]

    async def _val():
        return await get_valuation_async(ticker)

    response_data, analyst_rate_data, val = await asyncio.gather(_news(), _ratings(), _val())
    valuation_row = val[0] if val else {}
    return {
        "ticker": ticker,
        "news": response_data,
        "analystcoverage": analyst_rate_data,
        "valuation": valuation_row,
    }