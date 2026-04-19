"""Shared async HTTP client for outbound APIs (Alpha Vantage, StockNews, OpenRouter, etc.)."""

from __future__ import annotations

import httpx
from typing import Optional

_client: Optional[httpx.AsyncClient] = None


def build_default_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        limits=httpx.Limits(max_keepalive_connections=24, max_connections=100),
        timeout=httpx.Timeout(10.0, read=120.0, write=30.0, pool=5.0),
        headers={"User-Agent": "nxml-backend/1.0"},
    )


async def init_http_client() -> None:
    global _client
    if _client is None:
        _client = build_default_client()


async def close_http_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_http_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("HTTP client not initialized (app lifespan did not run)")
    return _client
