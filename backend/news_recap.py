"""Weekly news recap: yfinance ingest + OpenRouter gpt-4o-mini map–reduce."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Optional, Tuple

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ValidationError
from rapidfuzz import fuzz

import http_client
import db

load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)

NEWS_RECAP_MODEL = os.getenv("NEWS_RECAP_OR_MODEL", "openai/gpt-4o-mini")
MARKET_BASKET = tuple(
    s.strip().upper()
    for s in os.getenv("NEWS_MARKET_BASKET", "SPY,QQQ,IWM,DIA,GLD,TLT").split(",")
    if s.strip()
)
MAX_ARTICLES = int(os.getenv("NEWS_RECAP_MAX_ARTICLES", "18"))
SEM_LLM = int(os.getenv("NEWS_RECAP_SEM", "8"))
CACHE_TTL_ARTICLES = float(os.getenv("NEWS_RECAP_TTL_ARTICLES_SEC", "1800"))
CACHE_TTL_FULL = float(os.getenv("NEWS_RECAP_TTL_FULL_SEC", "21600"))

_full_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_articles_cache: Dict[str, Tuple[float, List[Dict[str, Any]]]] = {}
_cache_lock = asyncio.Lock()
_digest_sem = asyncio.Semaphore(SEM_LLM)


class ArticleDigest(BaseModel):
    article_id: str
    key_facts: List[str] = Field(default_factory=list)
    why_it_matters: str = ""
    risks_uncertainties: str = ""
    tickers_or_themes: List[str] = Field(default_factory=list)
    sentiment_hint: str = ""
    confidence: str = "medium"


class WeekRecapAI(BaseModel):
    week_summary_markdown: str
    themes: List[str] = Field(default_factory=list)
    watch_items: List[str] = Field(default_factory=list)
    disagreements_or_noise: Optional[str] = None


def _week_bucket() -> str:
    d = datetime.now(timezone.utc).date()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def _norm_title(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").lower().strip())


def _dedupe_articles(items: List[Dict[str, Any]], max_n: int) -> List[Dict[str, Any]]:
    seen_urls: set[str] = set()
    out: List[Dict[str, Any]] = []
    for a in sorted(items, key=lambda x: x.get("published_at") or "", reverse=True):
        url = (a.get("url") or "").strip()
        if url and url in seen_urls:
            continue
        title_n = _norm_title(a.get("title") or "")
        dup = False
        for b in out:
            if fuzz.token_set_ratio(title_n, _norm_title(b.get("title") or "")) >= 88:
                dup = True
                break
        if dup:
            continue
        if url:
            seen_urls.add(url)
        out.append(a)
        if len(out) >= max_n:
            break
    return out


def _yf_news_sync(symbol: str) -> List[dict]:
    import yfinance as yf

    t = yf.Ticker(symbol)
    if hasattr(t, "get_news"):
        return list(t.get_news(count=40, tab="all") or [])
    return list(t.news or [])


async def yfinance_news_for_symbol(symbol: str) -> List[dict]:
    try:
        return await asyncio.to_thread(_yf_news_sync, symbol)
    except ModuleNotFoundError as exc:
        logger.warning("yfinance dependency missing while loading %s news: %s", symbol, exc)
        return []
    except Exception as exc:  # noqa: BLE001
        logger.warning("yfinance news fetch failed for %s: %s", symbol, exc)
        return []


def _parse_publish_time(raw: Dict[str, Any]) -> Optional[datetime]:
    content = raw.get("content") if isinstance(raw.get("content"), dict) else {}
    candidates: List[Any] = [
        raw.get("providerPublishTime"),
        raw.get("pubDate"),
        content.get("pubDate"),
        content.get("displayTime"),
    ]

    for candidate in candidates:
        if candidate in (None, ""):
            continue
        if isinstance(candidate, (int, float)):
            # yfinance may provide seconds or milliseconds.
            ts = float(candidate)
            if ts > 10_000_000_000:
                ts /= 1000.0
            try:
                return datetime.fromtimestamp(int(ts), tz=timezone.utc)
            except (OSError, OverflowError, ValueError):
                continue

        text = str(candidate).strip()
        if not text:
            continue
        if text.isdigit():
            ts = float(text)
            if ts > 10_000_000_000:
                ts /= 1000.0
            try:
                return datetime.fromtimestamp(int(ts), tz=timezone.utc)
            except (OSError, OverflowError, ValueError):
                continue
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _extract_related_tickers(raw: Dict[str, Any]) -> List[str]:
    content = raw.get("content") if isinstance(raw.get("content"), dict) else {}
    direct = raw.get("relatedTickers")
    if isinstance(direct, list) and direct:
        return [str(x).strip().upper() for x in direct if str(x).strip()]

    finance = content.get("finance") if isinstance(content.get("finance"), dict) else {}
    stock_tickers = finance.get("stockTickers") if isinstance(finance, dict) else None
    if isinstance(stock_tickers, list):
        out: List[str] = []
        for item in stock_tickers:
            if isinstance(item, dict):
                sym = (
                    item.get("symbol")
                    or item.get("ticker")
                    or item.get("displaySymbol")
                    or ""
                )
            else:
                sym = item
            sym_s = str(sym).strip().upper()
            if sym_s:
                out.append(sym_s)
        if out:
            return out
    return []


def _extract_thumbnail_url(raw: Dict[str, Any]) -> str:
    content = raw.get("content") if isinstance(raw.get("content"), dict) else {}
    candidates: List[Any] = [
        raw.get("thumbnail"),
        content.get("thumbnail"),
        content.get("image"),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
        if isinstance(candidate, dict):
            direct = candidate.get("url")
            if isinstance(direct, str) and direct.strip():
                return direct.strip()
            resolutions = candidate.get("resolutions")
            if isinstance(resolutions, list):
                best_url = ""
                best_area = -1
                for item in resolutions:
                    if not isinstance(item, dict):
                        continue
                    url = str(item.get("url") or "").strip()
                    if not url:
                        continue
                    w = item.get("width")
                    h = item.get("height")
                    area = int(w or 0) * int(h or 0)
                    if area > best_area:
                        best_area = area
                        best_url = url
                if best_url:
                    return best_url
    return ""


def _normalize_yf_row(raw: Dict[str, Any], context_symbol: str) -> Optional[Dict[str, Any]]:
    content = raw.get("content") if isinstance(raw.get("content"), dict) else {}
    dt = _parse_publish_time(raw)
    if dt is None:
        return None
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    if dt < cutoff:
        return None

    click_through = (
        content.get("clickThroughUrl") if isinstance(content.get("clickThroughUrl"), dict) else {}
    )
    canonical_url = (
        content.get("canonicalUrl") if isinstance(content.get("canonicalUrl"), dict) else {}
    )
    provider = content.get("provider") if isinstance(content.get("provider"), dict) else {}

    link = str(
        raw.get("link")
        or click_through.get("url")
        or canonical_url.get("url")
        or ""
    ).strip()
    title = str(raw.get("title") or content.get("title") or "").strip()
    if not title and not link:
        return None

    publisher = str(
        raw.get("publisher")
        or provider.get("displayName")
        or provider.get("name")
        or ""
    ).strip()
    snippet = str(content.get("summary") or raw.get("summary") or "").strip()

    return {
        "id": str(raw.get("uuid") or content.get("id") or link or title)[:200],
        "title": title,
        "url": link,
        "publisher": publisher,
        "published_at": dt.isoformat(),
        "related_tickers": _extract_related_tickers(raw),
        "source_symbol": context_symbol,
        "snippet": snippet,
        "thumbnail_url": _extract_thumbnail_url(raw),
    }


async def ingest_ticker(ticker: str) -> List[Dict[str, Any]]:
    sym = ticker.strip().upper()
    rows = await yfinance_news_for_symbol(sym)
    norm: List[Dict[str, Any]] = []
    for r in rows:
        n = _normalize_yf_row(r, sym)
        if n:
            norm.append(n)
    return _dedupe_articles(norm, MAX_ARTICLES)


async def ingest_market() -> List[Dict[str, Any]]:
    batches = await asyncio.gather(*(yfinance_news_for_symbol(s) for s in MARKET_BASKET))
    merged: List[Dict[str, Any]] = []
    for sym, rows in zip(MARKET_BASKET, batches):
        for r in rows:
            n = _normalize_yf_row(r, sym)
            if n:
                merged.append(n)
    merged.sort(key=lambda x: x["published_at"], reverse=True)
    return _dedupe_articles(merged, MAX_ARTICLES)


async def _cache_get(store: Dict[str, Tuple[float, Any]], key: str) -> Optional[Any]:
    async with _cache_lock:
        hit = store.get(key)
        if not hit:
            return None
        exp, val = hit
        if time.monotonic() > exp:
            del store[key]
            return None
        return val


async def _cache_set(store: Dict[str, Tuple[float, Any]], key: str, val: Any, ttl: float) -> None:
    async with _cache_lock:
        store[key] = (time.monotonic() + ttl, val)


def _extract_json_text(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z0-9]*", "", text)
        text = text.strip().strip("`").strip()
    return text


async def _openrouter_chat(messages: List[Dict[str, str]], max_tokens: int) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise LookupError("OPENROUTER_API_KEY not configured")
    client = http_client.get_http_client()
    body: Dict[str, Any] = {
        "model": NEWS_RECAP_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    r = await client.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv(
                "OPENROUTER_HTTP_REFERER", "https://github.com/nxml/nxml"
            ),
            "X-Title": "nxml-news-recap",
        },
        json=body,
        timeout=httpx.Timeout(30.0, read=90.0),
    )
    r.raise_for_status()
    data = r.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Bad OpenRouter response: {e}") from e


def _fallback_digest(aid: str, article: Dict[str, Any]) -> ArticleDigest:
    return ArticleDigest(
        article_id=aid,
        key_facts=[(article.get("title") or "Untitled")[:200]],
        why_it_matters="Model output was not parseable; see title and URL for context.",
        risks_uncertainties="",
        tickers_or_themes=[str(x) for x in (article.get("related_tickers") or [])][:8],
        sentiment_hint="neutral",
        confidence="low",
    )


async def _digest_article(article: Dict[str, Any], idx: int) -> ArticleDigest:
    aid = str(article.get("id") or f"a{idx}")
    user = json.dumps(
        {
            "article_id": aid,
            "title": article.get("title"),
            "publisher": article.get("publisher"),
            "published_at": article.get("published_at"),
            "url": article.get("url"),
            "related_tickers": article.get("related_tickers"),
            "context_symbol": article.get("source_symbol"),
        },
        ensure_ascii=False,
    )
    sys = (
        "You are a financial news analyst. Given ONLY metadata for one article, "
        "extract structured insights. Do not invent events or quotes not implied by the title. "
        "Return a single JSON object with keys: article_id, key_facts (array of 2-5 short strings), "
        "why_it_matters (1-3 sentences), risks_uncertainties (1-2 sentences), "
        "tickers_or_themes (array of strings), sentiment_hint (one of: positive, negative, mixed, neutral), "
        "confidence (one of: low, medium, high)."
    )
    async with _digest_sem:
        raw = await _openrouter_chat(
            [{"role": "system", "content": sys}, {"role": "user", "content": user}],
            max_tokens=400,
        )
    try:
        payload = json.loads(_extract_json_text(raw))
        payload["article_id"] = aid
        return ArticleDigest.model_validate(payload)
    except (json.JSONDecodeError, ValidationError):
        repair_sys = (
            "Convert the user text into a single valid JSON object with keys: "
            "article_id, key_facts, why_it_matters, risks_uncertainties, "
            "tickers_or_themes, sentiment_hint, confidence. JSON only."
        )
        try:
            async with _digest_sem:
                raw2 = await _openrouter_chat(
                    [
                        {"role": "system", "content": repair_sys},
                        {"role": "user", "content": raw[:8000]},
                    ],
                    max_tokens=500,
                )
            payload = json.loads(_extract_json_text(raw2))
            payload["article_id"] = aid
            return ArticleDigest.model_validate(payload)
        except (json.JSONDecodeError, ValidationError, RuntimeError):
            return _fallback_digest(aid, article)


async def _map_all(articles: List[Dict[str, Any]]) -> List[ArticleDigest]:
    if not articles:
        return []
    tasks = [_digest_article(a, i) for i, a in enumerate(articles)]
    return await asyncio.gather(*tasks)


def _compact_digests(digests: List[ArticleDigest]) -> str:
    slim = []
    for d in digests:
        slim.append(
            {
                "article_id": d.article_id,
                "key_facts": d.key_facts[:5],
                "why_it_matters": d.why_it_matters[:500],
                "risks_uncertainties": d.risks_uncertainties[:400],
                "tickers_or_themes": d.tickers_or_themes[:12],
                "sentiment_hint": d.sentiment_hint,
                "confidence": d.confidence,
            }
        )
    return json.dumps(slim, ensure_ascii=False)[:100000]


async def _reduce_recap(
    scope_label: str, articles: List[Dict[str, Any]], digests: List[ArticleDigest]
) -> WeekRecapAI:
    digest_json = _compact_digests(digests)
    sys = (
        "You synthesize weekly market/ticker news from pre-digested article JSON. "
        "Do not add facts not present in the digests. Avoid buy/sell advice. "
        "Return JSON with keys: week_summary_markdown (string, markdown with headings), "
        "themes (array of short strings), watch_items (array of short strings), "
        "disagreements_or_noise (nullable string)."
    )
    meta = [
        {"title": a.get("title"), "url": a.get("url"), "publisher": a.get("publisher")}
        for a in articles[:30]
    ]
    user = (
        f"Scope: {scope_label}\nArticle listing (for alignment, do not contradict digests):\n"
        + json.dumps(meta, ensure_ascii=False)[:20000]
        + "\n\nDigests:\n"
        + digest_json
    )
    raw = await _openrouter_chat(
        [{"role": "system", "content": sys}, {"role": "user", "content": user}],
        max_tokens=1200,
    )
    try:
        return WeekRecapAI.model_validate(json.loads(_extract_json_text(raw)))
    except (json.JSONDecodeError, ValidationError, TypeError):
        return WeekRecapAI(
            week_summary_markdown=(
                "## Week in review\n\n_Summary synthesis was unavailable; "
                "use the per-article digests and article links below._"
            ),
            themes=[],
            watch_items=[],
            disagreements_or_noise="reduce_step_parse_failed",
        )


async def _persist_recap_db(kind: str, sym_key: str, week: str, out: Dict[str, Any]) -> None:
    try:
        store = {k: v for k, v in out.items() if k != "cache"}
        await db.upsert_llm_cache(kind, sym_key, week, store, NEWS_RECAP_MODEL)
    except Exception as exc:  # noqa: BLE001
        logger.warning("llm_cache upsert failed: %s", exc)


async def build_recap_payload(scope: Literal["market", "ticker"], ticker_upper: str) -> Dict[str, Any]:
    week = _week_bucket()
    sym_key = ticker_upper or "MARKET"
    kind = "news_recap_ticker" if scope == "ticker" else "news_recap_market"

    row_db = await db.fetch_llm_cache_row(kind, sym_key, week)
    if row_db and not db.is_llm_cache_stale(row_db) and isinstance(row_db.get("payload"), dict):
        out = dict(row_db["payload"])
        out["cache"] = {"hit": True, "layer": "db", "articles_layer_hit": True}
        return out

    cache_full_key = f"full:{scope}:{sym_key}:{week}"
    hit = await _cache_get(_full_cache, cache_full_key)
    if hit is not None:
        out = dict(hit)
        out["cache"] = {"hit": True, "layer": "full"}
        return out

    art_key = f"articles:{scope}:{sym_key}:{week}"
    articles: Optional[List[Dict[str, Any]]] = await _cache_get(_articles_cache, art_key)
    cache_articles_hit = articles is not None
    if articles is None:
        if scope == "market":
            articles = await ingest_market()
        else:
            articles = await ingest_ticker(ticker_upper)
        await _cache_set(_articles_cache, art_key, articles, CACHE_TTL_ARTICLES)

    if not articles:
        empty_out: Dict[str, Any] = {
            "scope": scope,
            "ticker": ticker_upper if scope == "ticker" else None,
            "articles": [],
            "ai": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "week_start": week,
                "model": NEWS_RECAP_MODEL,
                "recap_md": "",
                "themes": [],
                "watch_items": [],
                "per_article": [],
                "disagreements_or_noise": None,
                "error": "No yfinance headlines in the last 7 days for this scope.",
            },
            "cache": {"hit": False, "articles_layer_hit": cache_articles_hit},
        }
        await _persist_recap_db(kind, sym_key, week, empty_out)
        return empty_out

    scope_label = (
        f"Broad market basket {', '.join(MARKET_BASKET)}"
        if scope == "market"
        else f"Ticker {ticker_upper}"
    )

    ai_block: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "week_start": week,
        "model": NEWS_RECAP_MODEL,
        "recap_md": "",
        "themes": [],
        "watch_items": [],
        "per_article": [],
        "disagreements_or_noise": None,
        "error": None,
    }

    if os.getenv("OPENROUTER_API_KEY"):
        try:
            digests = await _map_all(articles)
            recap = await _reduce_recap(scope_label, articles, digests)
            ai_block["recap_md"] = recap.week_summary_markdown
            ai_block["themes"] = recap.themes
            ai_block["watch_items"] = recap.watch_items
            ai_block["disagreements_or_noise"] = recap.disagreements_or_noise
            ai_block["per_article"] = [d.model_dump() for d in digests]
        except Exception as exc:  # noqa: BLE001
            ai_block["error"] = str(exc)
    else:
        ai_block["error"] = "OPENROUTER_API_KEY not configured"

    out: Dict[str, Any] = {
        "scope": scope,
        "ticker": ticker_upper if scope == "ticker" else None,
        "articles": articles,
        "ai": ai_block,
        "cache": {"hit": False, "articles_layer_hit": cache_articles_hit},
    }
    if ai_block.get("error") is None:
        await _cache_set(_full_cache, cache_full_key, out, CACHE_TTL_FULL)
        await _persist_recap_db(kind, sym_key, week, out)
    return out


@router.get("/recap/market")
async def recap_market():
    return await build_recap_payload("market", "")


@router.get("/recap/{ticker}")
async def recap_ticker_path(ticker: str):
    sym = (ticker or "").strip().upper()
    if not sym or len(sym) > 8 or not sym.replace(".", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid ticker")
    if sym == "MARKET":
        raise HTTPException(status_code=400, detail="Reserved path; use /news/recap/market")
    return await build_recap_payload("ticker", sym)
