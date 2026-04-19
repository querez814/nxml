"""Async Postgres connection pool and valuation snapshot helpers.

The pool is lazy-initialized on first use so the rest of the app keeps working
if DATABASE_URL is unset or Railway is unreachable. Callers should treat
`get_pool()` returning None as "no cache available, compute on demand".
"""
from __future__ import annotations

import asyncio
import json
import logging
import math
import os
from datetime import date, datetime, timedelta, timezone
from typing import Any, Awaitable, Callable, Dict, List, Optional

import asyncpg
import dotenv as env

env.load_dotenv()

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.Pool] = None
_pool_lock = asyncio.Lock()
_pool_init_failed = False
_singleflight_lock = asyncio.Lock()
_singleflight_futures: Dict[str, asyncio.Future] = {}

# Reference to the FastAPI/uvicorn main event loop. Set from app startup via
# ``set_main_loop``. Used by ``sync_wait_awaitable`` so that sync code running
# in worker threads (e.g. ``run_in_executor`` / ``asyncio.to_thread``) can
# schedule DB-using coroutines back onto the loop that owns the asyncpg pool.
# Without this, ``asyncio.run`` would create a throwaway loop per call, and the
# pool (bound to the main loop) would crash with "Event loop is closed".
_main_loop: Optional[asyncio.AbstractEventLoop] = None


def set_main_loop(loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
    """Record the primary event loop so worker-thread sync helpers can target it."""
    global _main_loop
    if loop is None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
    _main_loop = loop


def _pool_loop_is_usable(pool: asyncpg.Pool) -> bool:
    """True if the pool's bound event loop is still alive and matches our main loop."""
    loop = getattr(pool, "_loop", None)
    if loop is None:
        return True  # be permissive; let asyncpg decide
    if loop.is_closed():
        return False
    if _main_loop is not None and loop is not _main_loop:
        return False
    return True


def _is_connection_lost_error(exc: Exception) -> bool:
    if isinstance(exc, (asyncpg.exceptions.ConnectionDoesNotExistError, ConnectionError, OSError)):
        return True
    msg = str(exc).lower()
    return "connection was closed" in msg or "connection does not exist" in msg


async def _reset_pool_for_reconnect() -> None:
    """Drop the current pool so the next operation recreates it."""
    global _pool, _pool_init_failed
    old_pool: Optional[asyncpg.Pool] = None
    async with _pool_lock:
        old_pool = _pool
        _pool = None
        # Allow re-init after transient network / server blips.
        _pool_init_failed = False
    if old_pool is not None:
        try:
            await old_pool.close()
        except Exception:
            pass

def _snapshot_stale_after() -> timedelta:
    """How long snapshot rows stay 'fresh' before a read may trigger an AV refresh.

    Default 14 days so routine traffic uses Railway Postgres instead of Alpha Vantage.
    Override with ``VALUATION_SNAPSHOT_STALE_HOURS`` (e.g. ``24`` for daily refresh).
    """
    raw = os.getenv("VALUATION_SNAPSHOT_STALE_HOURS", "336").strip()
    try:
        hours = float(raw)
    except ValueError:
        hours = 336.0
    if hours <= 0:
        hours = 336.0
    return timedelta(hours=hours)


def is_stale(row: Optional[Dict[str, Any]]) -> bool:
    if row is None:
        return True
    as_of = row.get("as_of_date")
    if as_of is None:
        return True
    if isinstance(as_of, datetime):
        reference = datetime.now(timezone.utc) if as_of.tzinfo else datetime.utcnow()
        return (reference - as_of) > _snapshot_stale_after()
    return True

SNAPSHOT_COLUMNS: List[str] = [
    "symbol", "fiscal_date_ending", "as_of_date", "sector", "industry",
    "shares_outstanding", "market_cap", "enterprise_value", "adjusted_price",
    "latest_closing_price", "latest_market_cap", "latest_enterprise_value",
    "pe_ratio", "pe_fwd", "pe_fwd_nongaap", "peg_ratio", "peg_nongaap_fwd",
    "ps_ttm", "ps_fwd", "pb_ratio", "price_to_cash_flow_ttm", "price_to_fcf_ttm",
    "ev_to_revenue", "ev_to_sales_fwd", "ev_to_ebitda", "ev_to_ebit",
    "ev_to_gross_profit", "ev_to_fcf_ttm", "ev_to_net_income",
    "dividend_yield", "dividend_yield_ttm", "dividend_per_share", "payout_ratio",
    "profit_margin", "operating_margin_ttm", "roa_ttm", "roe_ttm",
    "book_value_per_share", "diluted_eps_ttm", "revenue_per_share_ttm",
    "rev_growth_yoy", "eps_growth_yoy",
    "beta", "week52_high", "week52_low", "ma_50d", "ma_200d",
    "analyst_target_price", "analyst_rating_strong_buy", "analyst_rating_buy",
    "analyst_rating_hold", "analyst_rating_sell", "analyst_rating_strong_sell",
]

FIVE_Y_COLUMNS: List[str] = [
    "pe_ratio_5y", "pe_fwd_5y", "ps_ttm_5y", "pb_ratio_5y",
    "ev_to_revenue_5y", "ev_to_ebitda_5y", "ev_to_ebit_5y",
    "ev_to_gross_profit_5y", "price_to_fcf_5y", "ev_to_fcf_5y",
    "dividend_yield_5y",
]

_5Y_SOURCE_MAP = {
    "pe_ratio_5y":          "pe_ratio",
    "pe_fwd_5y":            "pe_fwd",
    "ps_ttm_5y":            "ps_ttm",
    "pb_ratio_5y":          "pb_ratio",
    "ev_to_revenue_5y":     "ev_to_revenue",
    "ev_to_ebitda_5y":      "ev_to_ebitda",
    "ev_to_ebit_5y":        "ev_to_ebit",
    "ev_to_gross_profit_5y": "ev_to_gross_profit",
    "price_to_fcf_5y":      "price_to_fcf_ttm",
    "ev_to_fcf_5y":         "ev_to_fcf_ttm",
    "dividend_yield_5y":    "dividend_yield",
}


async def get_pool() -> Optional[asyncpg.Pool]:
    """Return a shared pool, or None if DB is unavailable."""
    global _pool, _pool_init_failed
    if _pool is not None and not _pool_loop_is_usable(_pool):
        # Pool was bound to a now-closed (or wrong) loop. Discard it so we can
        # rebuild on the current loop. Reset failure flag so init can retry.
        logger.warning("DB pool was bound to a stale event loop; rebuilding.")
        try:
            await _pool.close()
        except Exception:
            pass
        _pool = None
        _pool_init_failed = False
    if _pool_init_failed:
        return None
    if _pool is not None:
        return _pool
    async with _pool_lock:
        if _pool is not None and _pool_loop_is_usable(_pool):
            return _pool
        dsn = os.getenv("DATABASE_URL")
        if not dsn:
            logger.warning("DATABASE_URL not set; valuation cache disabled.")
            _pool_init_failed = True
            return None
        try:
            _pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=1,
                max_size=5,
                init=_init_connection,
            )
        except Exception as exc:
            logger.warning("DB pool init failed (%s); valuation cache disabled.", exc)
            _pool_init_failed = True
            return None
    return _pool


def _jsonb_encode(value: Any) -> str:
    """Encode any Python value asyncpg hands us into a jsonb wire string.

    Our ``upsert_*`` helpers already pass a pre-serialized JSON string with an
    explicit ``$3::jsonb`` cast, so the encoder usually isn't invoked. But if
    asyncpg ever does invoke it (via type inference on prepared statements),
    we must NOT double-encode strings into ``"..."``.
    """
    if isinstance(value, str):
        return value
    return json.dumps(value, default=str, allow_nan=False)


async def _init_connection(conn: asyncpg.Connection) -> None:
    """Register codecs so jsonb columns are decoded to Python objects automatically.

    Without this, asyncpg returns jsonb as the raw JSON *string*, which then
    breaks downstream consumers like ``pd.DataFrame(...)`` in the valuation
    refresh chain.
    """
    for type_name in ("jsonb", "json"):
        try:
            await conn.set_type_codec(
                type_name,
                encoder=_jsonb_encode,
                decoder=json.loads,
                schema="pg_catalog",
                format="text",
            )
        except Exception as exc:  # noqa: BLE001 - codec setup is best-effort
            logger.warning("Failed to register %s codec on asyncpg connection: %s", type_name, exc)


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def fetch_snapshots(symbol: str) -> List[Dict[str, Any]]:
    """Return all cached snapshot rows for a symbol (newest first)."""
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return []
        try:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT * FROM valuation_snapshot WHERE symbol = $1 ORDER BY fiscal_date_ending DESC",
                    symbol,
                )
            return [dict(r) for r in rows]
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("fetch_snapshots reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise
    return []


async def latest_snapshot(symbol: str) -> Optional[Dict[str, Any]]:
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return None
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM valuation_snapshot WHERE symbol = $1 ORDER BY fiscal_date_ending DESC LIMIT 1",
                    symbol,
                )
            return dict(row) if row else None
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("latest_snapshot reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise
    return None


async def upsert_snapshots(rows: List[Dict[str, Any]]) -> None:
    """Insert-or-update a batch of snapshot rows (keyed by symbol + fiscal_date_ending)."""
    if not rows:
        return

    cols = SNAPSHOT_COLUMNS
    placeholders = ", ".join(f"${i + 1}" for i in range(len(cols)))
    update_cols = [c for c in cols if c not in ("symbol", "fiscal_date_ending")]
    update_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_cols)
    query = (
        f"INSERT INTO valuation_snapshot ({', '.join(cols)}) "
        f"VALUES ({placeholders}) "
        f"ON CONFLICT (symbol, fiscal_date_ending) DO UPDATE SET {update_clause}"
    )

    records = [tuple(_coerce(r.get(c)) for c in cols) for r in rows]

    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return
        try:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await conn.executemany(query, records)
            return
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("upsert_snapshots reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise


async def refresh_5y_avg(symbol: str) -> None:
    """Recompute the 5Y averages row for a symbol from snapshot data."""
    cutoff = date.today() - timedelta(days=365 * 5)
    avg_exprs = ", ".join(
        f"AVG(NULLIF({src}, 0)) AS {dest}" for dest, src in _5Y_SOURCE_MAP.items()
    )
    select_q = (
        f"SELECT {avg_exprs} FROM valuation_snapshot "
        f"WHERE symbol = $1 AND fiscal_date_ending >= $2"
    )

    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(select_q, symbol, cutoff)
                if row is None:
                    return
                dest_cols = list(_5Y_SOURCE_MAP.keys())
                insert_cols = ["symbol", "computed_at"] + dest_cols
                placeholders = ", ".join(f"${i + 1}" for i in range(len(insert_cols)))
                update_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in ["computed_at"] + dest_cols)
                query = (
                    f"INSERT INTO valuation_5y_avg ({', '.join(insert_cols)}) "
                    f"VALUES ({placeholders}) "
                    f"ON CONFLICT (symbol) DO UPDATE SET {update_clause}"
                )
                values = [symbol, datetime.now(timezone.utc)] + [_coerce(row[c]) for c in dest_cols]
                await conn.execute(query, *values)
            return
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("refresh_5y_avg reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise


async def fetch_5y_avg(symbol: str) -> Optional[Dict[str, Any]]:
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return None
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow("SELECT * FROM valuation_5y_avg WHERE symbol = $1", symbol)
            return dict(row) if row else None
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("fetch_5y_avg reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise
    return None


def _coerce(value: Any) -> Any:
    """Normalize numeric NaN/inf and pandas types into plain Python values asyncpg accepts."""
    if value is None:
        return None
    try:
        import numpy as np  # local import to avoid hard dep at import-time
        if isinstance(value, (np.integer,)):
            return int(value)
        if isinstance(value, (np.floating,)):
            v = float(value)
            return None if (v != v or v in (float("inf"), float("-inf"))) else v
    except Exception:
        pass
    if isinstance(value, float):
        return None if (value != value or value in (float("inf"), float("-inf"))) else value
    return value


# --- Financial statement JSON cache (see migrations/002_financial_and_ai_cache.sql) ---

DATASET_INCOME_QUARTERLY = "income_quarterly"
DATASET_INCOME_ANNUAL = "income_annual"
DATASET_BALANCE_QUARTERLY = "balance_quarterly"
DATASET_BALANCE_ANNUAL = "balance_annual"
DATASET_CASHFLOW_QUARTERLY = "cashflow_quarterly"
DATASET_CASHFLOW_ANNUAL = "cashflow_annual"


def _financial_cache_stale_after() -> timedelta:
    raw = os.getenv("FINANCIAL_CACHE_STALE_HOURS", "336").strip()
    try:
        hours = float(raw)
    except ValueError:
        hours = 336.0
    if hours <= 0:
        hours = 336.0
    return timedelta(hours=hours)


def is_financial_cache_row_stale(row: Optional[Dict[str, Any]]) -> bool:
    if row is None:
        return True
    fetched = row.get("fetched_at")
    if fetched is None:
        return True
    if isinstance(fetched, datetime):
        ref = datetime.now(timezone.utc) if fetched.tzinfo else datetime.utcnow()
        return (ref - fetched) > _financial_cache_stale_after()
    return True


def ensure_json_for_db(obj: Any) -> Any:
    """Recursively sanitize payloads into strict JSON-safe values.

    Postgres ``jsonb`` rejects non-standard JSON values like NaN/Infinity, so
    these are converted to ``None``. Datetime/date values are stringified.
    """

    def _sanitize(value: Any) -> Any:
        if value is None:
            return None

        # Convert numpy scalar wrappers to native Python values first.
        coerced = _coerce(value)
        if coerced is None:
            return None
        if isinstance(coerced, (str, bool, int)):
            return coerced
        if isinstance(coerced, float):
            return None if (math.isnan(coerced) or math.isinf(coerced)) else coerced
        if isinstance(coerced, (datetime, date)):
            return coerced.isoformat()
        if isinstance(coerced, dict):
            return {str(k): _sanitize(v) for k, v in coerced.items()}
        if isinstance(coerced, (list, tuple, set)):
            return [_sanitize(v) for v in coerced]

        # Final fallback for unknown non-JSON-native objects.
        return str(coerced)

    return _sanitize(obj)


def _decode_jsonb(value: Any) -> Any:
    """If the jsonb codec didn't run, asyncpg returns the raw JSON text. Parse it.

    Older cached rows or fresh pool connections without the codec installed will
    surface as strings; downstream consumers expect Python lists/dicts.
    """
    if isinstance(value, (bytes, bytearray, memoryview)):
        try:
            value = bytes(value).decode("utf-8")
        except Exception:
            return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


async def fetch_financial_cache_row(symbol: str, dataset: str) -> Optional[Dict[str, Any]]:
    sym = (symbol or "").strip().upper()
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return None
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT symbol, dataset, payload, fetched_at, latest_fiscal_date, source_note "
                    "FROM financial_statement_cache WHERE symbol = $1 AND dataset = $2",
                    sym,
                    dataset,
                )
            if row is None:
                return None
            out = dict(row)
            out["payload"] = _decode_jsonb(out.get("payload"))
            return out
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("fetch_financial_cache_row reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise
    return None


async def upsert_financial_cache(
    symbol: str,
    dataset: str,
    payload: Any,
    latest_fiscal_date: Optional[date] = None,
    source_note: Optional[str] = None,
) -> None:
    sym = (symbol or "").strip().upper()
    safe = ensure_json_for_db(payload)
    payload_json = json.dumps(safe, default=str, allow_nan=False)
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return
        try:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO financial_statement_cache
                      (symbol, dataset, payload, fetched_at, latest_fiscal_date, source_note)
                    VALUES ($1, $2, $3::jsonb, now(), $4, $5)
                    ON CONFLICT (symbol, dataset) DO UPDATE SET
                      payload = EXCLUDED.payload,
                      fetched_at = EXCLUDED.fetched_at,
                      latest_fiscal_date = EXCLUDED.latest_fiscal_date,
                      source_note = EXCLUDED.source_note
                    """,
                    sym,
                    dataset,
                    payload_json,
                    latest_fiscal_date,
                    source_note,
                )
            return
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("upsert_financial_cache reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise


# --- LLM / news recap cache ---

def _llm_cache_ttl() -> timedelta:
    raw = os.getenv("LLM_CACHE_TTL_HOURS", "168").strip()
    try:
        hours = float(raw)
    except ValueError:
        hours = 168.0
    if hours <= 0:
        hours = 168.0
    return timedelta(hours=hours)


def is_llm_cache_stale(row: Optional[Dict[str, Any]]) -> bool:
    if row is None:
        return True
    exp = row.get("expires_at")
    if isinstance(exp, datetime):
        ref = datetime.now(timezone.utc) if exp.tzinfo else datetime.utcnow()
        if ref > exp:
            return True
    created = row.get("created_at")
    if isinstance(created, datetime):
        ref = datetime.now(timezone.utc) if created.tzinfo else datetime.utcnow()
        return (ref - created) > _llm_cache_ttl()
    return True


async def fetch_llm_cache_row(
    cache_kind: str, symbol: str, context_key: str
) -> Optional[Dict[str, Any]]:
    sym = symbol or ""
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return None
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT cache_kind, symbol, context_key, payload, model, created_at, expires_at "
                    "FROM llm_cache WHERE cache_kind = $1 AND symbol = $2 AND context_key = $3",
                    cache_kind,
                    sym,
                    context_key,
                )
            if row is None:
                return None
            out = dict(row)
            out["payload"] = _decode_jsonb(out.get("payload"))
            return out
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("fetch_llm_cache_row reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise
    return None


async def upsert_llm_cache(
    cache_kind: str,
    symbol: str,
    context_key: str,
    payload: Any,
    model: Optional[str] = None,
) -> None:
    safe = ensure_json_for_db(payload)
    payload_json = json.dumps(safe, default=str, allow_nan=False)
    ttl = _llm_cache_ttl()
    expires = datetime.now(timezone.utc) + ttl
    sym = symbol or ""
    for attempt in range(2):
        pool = await get_pool()
        if pool is None:
            return
        try:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO llm_cache
                      (cache_kind, symbol, context_key, payload, model, created_at, expires_at)
                    VALUES ($1, $2, $3, $4::jsonb, $5, now(), $6)
                    ON CONFLICT (cache_kind, symbol, context_key) DO UPDATE SET
                      payload = EXCLUDED.payload,
                      model = EXCLUDED.model,
                      created_at = EXCLUDED.created_at,
                      expires_at = EXCLUDED.expires_at
                    """,
                    cache_kind,
                    sym,
                    context_key,
                    payload_json,
                    model,
                    expires,
                )
            return
        except Exception as exc:
            if attempt == 0 and _is_connection_lost_error(exc):
                logger.warning("upsert_llm_cache reconnect after dropped DB connection: %s", exc)
                await _reset_pool_for_reconnect()
                continue
            raise


def sync_wait_awaitable(factory: Callable[[], Any]) -> Any:
    """Run an async coroutine from sync code.

    Sync helpers in ``backend/fetch/*`` are frequently called from worker
    threads (e.g. via ``asyncio.to_thread`` / ``run_in_executor``). Naively
    running ``asyncio.run`` inside such a thread spins up a throwaway event
    loop, which the asyncpg pool cannot share with the FastAPI main loop and
    blows up with ``RuntimeError: Event loop is closed``.

    Strategy:
    1. If the FastAPI main loop is known and running, schedule the coroutine
       there via ``run_coroutine_threadsafe`` (works from any worker thread).
    2. If we're *on* the main loop already, fall back to a temporary worker
       thread + ``asyncio.run`` so we don't deadlock by blocking the loop.
    3. Otherwise (e.g. CLI / scripts with no loop anywhere), just
       ``asyncio.run`` here.
    """

    def _runner_in_new_loop() -> Any:
        return asyncio.run(factory())

    main_loop = _main_loop
    if main_loop is not None and not main_loop.is_closed() and main_loop.is_running():
        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None
        if current is main_loop:
            # Calling sync_wait_awaitable from within the main loop would
            # deadlock; offload to a worker thread with its own loop.
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                return ex.submit(_runner_in_new_loop).result()
        # Schedule on the main loop (works whether we're in another worker
        # thread or have no loop at all).
        future = asyncio.run_coroutine_threadsafe(factory(), main_loop)
        return future.result()

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return _runner_in_new_loop()
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        return ex.submit(_runner_in_new_loop).result()


def latest_fiscal_date_from_statement_rows(rows: Any) -> Optional[date]:
    """Max fiscalDateEnding from a list of quarterly/annual statement dicts."""
    if not rows or not isinstance(rows, list):
        return None
    best: Optional[date] = None
    for row in rows:
        if not isinstance(row, dict):
            continue
        raw = row.get("fiscalDateEnding")
        if not raw:
            continue
        try:
            if isinstance(raw, datetime):
                d = raw.date()
            else:
                s = str(raw).strip()[:10]
                d = date.fromisoformat(s)
        except (TypeError, ValueError):
            continue
        if best is None or d > best:
            best = d
    return best


def analysis_context_key(symbol: str, latest_fiscal: Optional[str]) -> str:
    """Stable key: new quarter filing invalidates cache."""
    sym = (symbol or "").strip().upper()
    fd = (latest_fiscal or "").strip()
    return f"{sym}:{fd}"


async def run_singleflight(key: str, producer: Callable[[], Awaitable[Any]]) -> Any:
    """Ensure concurrent callers for the same key share one in-flight producer."""
    wait_on: Optional[asyncio.Future] = None
    async with _singleflight_lock:
        existing = _singleflight_futures.get(key)
        if existing is not None:
            wait_on = existing
        else:
            loop = asyncio.get_running_loop()
            fut: asyncio.Future = loop.create_future()
            fut.add_done_callback(lambda f: f.exception() if f.done() and not f.cancelled() else None)
            _singleflight_futures[key] = fut
            wait_on = None

    if wait_on is not None:
        return await wait_on

    try:
        value = await producer()
    except Exception as exc:
        fut.set_exception(exc)
        raise
    else:
        fut.set_result(value)
        return value
    finally:
        async with _singleflight_lock:
            _singleflight_futures.pop(key, None)
