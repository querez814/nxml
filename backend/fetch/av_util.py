"""Alpha Vantage JSON helpers for sync `requests` call paths."""

from __future__ import annotations

import asyncio
import os
import random
import threading
import time
from typing import Any, Mapping, Optional

import requests as r

from fastapi import HTTPException

import http_client

_AV_MAX_PARALLEL_SYNC = max(1, int(os.getenv("AV_MAX_PARALLEL_SYNC", "2")))
_AV_MIN_INTERVAL_SYNC = max(0.0, float(os.getenv("AV_MIN_INTERVAL_SYNC_SEC", "0.35")))
_AV_MAX_PARALLEL_ASYNC = max(1, int(os.getenv("AV_MAX_PARALLEL_ASYNC", "3")))
_AV_MIN_INTERVAL_ASYNC = max(0.0, float(os.getenv("AV_MIN_INTERVAL_ASYNC_SEC", "0.25")))

_sync_gate = threading.Semaphore(_AV_MAX_PARALLEL_SYNC)
_sync_lock = threading.Lock()
_sync_next_allowed = 0.0

_async_gate = asyncio.Semaphore(_AV_MAX_PARALLEL_ASYNC)
_async_lock = asyncio.Lock()
_async_next_allowed = 0.0


def raise_if_av_blocked(data: Mapping[str, Any]) -> None:
    """Raise HTTP 429 when AV returns throttle or error meta keys instead of payload rows.

    Call this immediately after ``response.json()`` (and successful HTTP status)
    before treating empty ``quarterlyReports`` / similar as 404.
    """
    if not isinstance(data, dict):
        return
    if "Error Message" in data:
        raise HTTPException(
            status_code=429,
            detail=str(data.get("Error Message") or "Alpha Vantage error"),
        )
    if "Note" in data:
        raise HTTPException(
            status_code=429,
            detail=str(data.get("Note") or "Alpha Vantage rate limit"),
        )
    if "Information" in data:
        raise HTTPException(
            status_code=429,
            detail=str(data.get("Information") or "Alpha Vantage information"),
        )


def _sync_wait_for_slot() -> None:
    global _sync_next_allowed
    with _sync_lock:
        now = time.monotonic()
        wait_for = max(0.0, _sync_next_allowed - now)
        _sync_next_allowed = max(_sync_next_allowed, now) + _AV_MIN_INTERVAL_SYNC + random.uniform(0.0, 0.08)
    if wait_for > 0:
        time.sleep(wait_for)


async def _async_wait_for_slot() -> None:
    global _async_next_allowed
    async with _async_lock:
        now = time.monotonic()
        wait_for = max(0.0, _async_next_allowed - now)
        _async_next_allowed = max(_async_next_allowed, now) + _AV_MIN_INTERVAL_ASYNC + random.uniform(0.0, 0.08)
    if wait_for > 0:
        await asyncio.sleep(wait_for)


def av_get_json_sync(url: str, *, params: Optional[Mapping[str, Any]] = None, retries: int = 2) -> Mapping[str, Any]:
    """Global sync AV wrapper with jittered backoff and process-wide pacing."""
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            with _sync_gate:
                _sync_wait_for_slot()
                resp = r.get(url, params=params, timeout=30)
            if resp.status_code >= 500:
                raise HTTPException(status_code=resp.status_code, detail="Alpha Vantage upstream error")
            if resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")
            payload = resp.json()
            raise_if_av_blocked(payload)
            return payload
        except HTTPException as exc:
            last_error = exc
            is_retryable = exc.status_code in (429, 500, 502, 503, 504)
            if attempt >= retries or not is_retryable:
                raise
            time.sleep((0.6 * (2 ** attempt)) + random.uniform(0.05, 0.3))
        except Exception as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep((0.6 * (2 ** attempt)) + random.uniform(0.05, 0.3))
    raise HTTPException(status_code=500, detail=f"Alpha Vantage request failed: {last_error}")


async def av_get_json_async(url: str, *, retries: int = 2) -> Mapping[str, Any]:
    """Global async AV wrapper with jittered backoff and process-wide pacing."""
    client = http_client.get_http_client()
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            async with _async_gate:
                await _async_wait_for_slot()
                resp = await client.get(url)
            if resp.status_code >= 500:
                raise HTTPException(status_code=resp.status_code, detail="Alpha Vantage upstream error")
            if resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")
            payload = resp.json()
            raise_if_av_blocked(payload)
            return payload
        except HTTPException as exc:
            last_error = exc
            is_retryable = exc.status_code in (429, 500, 502, 503, 504)
            if attempt >= retries or not is_retryable:
                raise
            await asyncio.sleep((0.6 * (2 ** attempt)) + random.uniform(0.05, 0.3))
        except Exception as exc:
            last_error = exc
            if attempt >= retries:
                break
            await asyncio.sleep((0.6 * (2 ** attempt)) + random.uniform(0.05, 0.3))
    raise HTTPException(status_code=500, detail=f"Alpha Vantage request failed: {last_error}")
