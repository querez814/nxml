from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, TypeVar
import asyncio
import logging
import time
import random
import dotenv as env
import os
import math
import numpy as np
import pandas as pd

from fetch.prices import get_prices
from fetch.income_statement import build_ttm_quarters_response, get_quarterly_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
from fetch.cashflow import get_quarterly_cashflow_statement_data
from fetch.earnings_estimates import forward_eps_and_revenue
from fetch.dividends import ttm_dividend_sum
from fetch.summary import get_summary

from sector_rules import get_ratio_priority, label_for
import db

env.load_dotenv()
logger = logging.getLogger(__name__)
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

_T = TypeVar("_T")


def _with_av_retry(fn: Callable[[], _T], *, retries: int = 2, backoff_s: float = 1.2) -> _T:
    """On Alpha Vantage throttle (HTTP 429), retry with jittered backoff."""
    last: Optional[HTTPException] = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except HTTPException as exc:
            last = exc
            if exc.status_code == 429 and attempt < retries:
                time.sleep((backoff_s * (2 ** attempt)) + random.uniform(0.05, 0.4))
                continue
            raise
    assert last is not None
    raise last


# ---------- numeric helpers ----------

def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        if isinstance(value, str):
            if value.strip() in ("", "-", "None", "NM", "N/A"):
                return None
            value = value.replace(",", "")
        v = float(value)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except (TypeError, ValueError):
        return None


def _safe_div(num: Optional[float], denom: Optional[float]) -> Optional[float]:
    if num is None or denom is None or denom == 0:
        return None
    result = num / denom
    if math.isnan(result) or math.isinf(result):
        return None
    return round(result, 4)


def _clean_numeric_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)


def _normalize_row_payload(value: Any) -> List[Dict[str, Any]]:
    """Coerce a cache/AV payload into a list-of-dict shape pandas can ingest.

    asyncpg has historically returned ``jsonb`` columns as raw JSON strings when
    a codec is missing; we also occasionally see dict-shaped payloads from older
    code paths. Normalize so ``pd.DataFrame(...)`` can never blow up here.
    """
    import json as _json

    if value is None:
        return []
    if isinstance(value, (bytes, bytearray, memoryview)):
        try:
            value = bytes(value).decode("utf-8")
        except Exception:
            return []
    if isinstance(value, str):
        try:
            value = _json.loads(value)
        except (TypeError, ValueError):
            return []
    if isinstance(value, dict):
        rows = value.get("rows")
        if isinstance(rows, list):
            return [r for r in rows if isinstance(r, dict)]
        return [value]
    if isinstance(value, list):
        return [r for r in value if isinstance(r, dict)]
    return []


# ---------- capital structure ----------

def _build_cap_struct(ticker: str) -> pd.DataFrame:
    """Return one row per fiscalDateEnding with mc, ev, adjusted price, and the "latest" companion values."""
    bs_data = get_quarterly_balance_sheet_data(ticker)
    bs_rows = _normalize_row_payload(bs_data)
    if not bs_rows:
        raise HTTPException(status_code=404, detail="No balance sheet data available")
    bs = pd.DataFrame(bs_rows)
    if bs.empty:
        raise HTTPException(status_code=404, detail="No balance sheet data available")

    prices = get_prices(ticker)
    price_rows = _normalize_row_payload(prices)
    if not price_rows:
        raise HTTPException(status_code=404, detail="No price data available")
    prices = price_rows

    prices_df = pd.DataFrame(prices)
    prices_df["fiscalDateEnding"] = pd.to_datetime(prices_df["fiscalDateEnding"])
    prices_df = prices_df.sort_values("fiscalDateEnding", ascending=False)
    latest_closing_price = float(prices_df.iloc[0]["5. adjusted close"])

    bs["fiscalDateEnding"] = pd.to_datetime(bs["fiscalDateEnding"])

    def closest_close(d):
        match = prices_df[prices_df["fiscalDateEnding"] <= d].head(1)
        return float(match["5. adjusted close"].iloc[0]) if not match.empty else None

    bs["adjustedPrice"] = bs["fiscalDateEnding"].apply(closest_close)
    for col in ("commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "currentDebt"):
        bs[col] = _clean_numeric_series(bs[col])

    bs = bs.sort_values("fiscalDateEnding", ascending=False).reset_index(drop=True)

    latest_so = float(bs["commonStockSharesOutstanding"].iloc[0]) if pd.notna(bs["commonStockSharesOutstanding"].iloc[0]) else 0.0
    latest_cash = float(bs["cashAndCashEquivalentsAtCarryingValue"].iloc[0]) if pd.notna(bs["cashAndCashEquivalentsAtCarryingValue"].iloc[0]) else 0.0
    latest_debt = float(bs["currentDebt"].iloc[0]) if pd.notna(bs["currentDebt"].iloc[0]) else 0.0

    bs["mc"] = bs["commonStockSharesOutstanding"] * bs["adjustedPrice"]
    bs["ev"] = bs["mc"] + bs["cashAndCashEquivalentsAtCarryingValue"] + bs["currentDebt"]
    bs["latest_closing_price"] = latest_closing_price
    bs["latestMC"] = latest_so * latest_closing_price
    bs["latestEV"] = bs["latestMC"] + latest_cash + latest_debt

    cols = [
        "fiscalDateEnding", "commonStockSharesOutstanding", "adjustedPrice", "latest_closing_price",
        "cashAndCashEquivalentsAtCarryingValue", "currentDebt", "mc", "ev", "latestMC", "latestEV",
    ]
    return bs[cols].rename(columns={
        "commonStockSharesOutstanding": "sharesOutstanding",
        "cashAndCashEquivalentsAtCarryingValue": "cashCashEq",
    })


def _build_ttm_table(
    ticker: str, income_rows: Optional[List[Dict[str, Any]]] = None
) -> pd.DataFrame:
    """Quarterly TTM fundamentals per fiscalDateEnding. Pass ``income_rows`` to reuse one income fetch."""
    if income_rows is None:
        try:
            quarters = _with_av_retry(
                lambda: build_ttm_quarters_response(ticker, None)["quarters"]
            )
        except HTTPException as exc:
            if exc.status_code == 429:
                raise
            return pd.DataFrame()
    else:
        try:
            quarters = build_ttm_quarters_response(ticker, income_rows)["quarters"]
        except HTTPException as exc:
            if exc.status_code == 429:
                raise
            return pd.DataFrame()

    data = pd.DataFrame(quarters)
    if data.empty:
        return data

    wanted = {
        "totalRevenueTTM": "totalRevenue_ttm",
        "grossProfitTTM":  "grossProfit_ttm",
        "ebitTTM":         "ebit_ttm",
        "ebitdaTTM":       "ebitda_ttm",
        "operatingIncomeTTM": "operatingIncome_ttm",
        "netIncomeTTM":    "netIncome_ttm",
        "reportedEPSTTM":  "reportedEPS_ttm",
    }

    out = pd.DataFrame()
    out["fiscalDateEnding"] = pd.to_datetime(data["fiscalDateEnding"])
    for src, dest in wanted.items():
        if src in data.columns:
            out[dest] = pd.to_numeric(data[src], errors="coerce")
    return out.sort_values("fiscalDateEnding", ascending=False).reset_index(drop=True)


def _build_cashflow_ttm(
    ticker: str, income_records: Optional[List[Dict[str, Any]]] = None
) -> pd.DataFrame:
    """Returns fiscalDateEnding, operatingCashflow_ttm, freeCashFlow_ttm, dividendPayout_ttm."""
    try:
        rows = _with_av_retry(
            lambda: get_quarterly_cashflow_statement_data(ticker, income_records)
        )
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"])
    df = df.sort_values("fiscalDateEnding", ascending=False).reset_index(drop=True)

    for col in ("operatingCashflow", "freeCashFlow", "dividendPayout", "capitalExpenditures"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    out = pd.DataFrame()
    out["fiscalDateEnding"] = df["fiscalDateEnding"]
    for col in ("operatingCashflow", "freeCashFlow", "dividendPayout"):
        ttm = []
        if col in df.columns:
            for i in range(len(df)):
                ttm.append(df[col].iloc[i:i + 4].sum())
        else:
            ttm = [np.nan] * len(df)
        out[f"{col}_ttm"] = ttm
    return out


# ---------- the ratio engine ----------

def _compute_snapshot_rows(ticker: str) -> List[Dict[str, Any]]:
    """Build the full per-quarter snapshot list for a ticker. Pure compute (no DB)."""
    # OVERVIEW is best-effort: if AV is throttling or fails, keep going with whatever we have.
    # Without this, a single OVERVIEW failure used to bubble HTTPException(500) out of the
    # valuation route even though every other AV call here is already guarded.
    try:
        summary_json: Dict[str, Any] = dict(_with_av_retry(lambda: get_summary(ticker)))
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.warning(
            "valuation_refresh: OVERVIEW failed for %s, continuing without summary fields. detail=%s",
            ticker,
            getattr(exc, "detail", exc),
        )
        summary_json = {}
    except Exception as exc:
        logger.warning(
            "valuation_refresh: OVERVIEW raised %s for %s, continuing without summary fields.",
            type(exc).__name__,
            ticker,
        )
        summary_json = {}

    symbol = summary_json.get("Symbol") or ticker.upper()
    sector = summary_json.get("Sector")
    industry = summary_json.get("Industry")

    # Pass-through ratios from AV OVERVIEW (TTM / forward values, not per-quarter historical)
    av_ratios = {
        "pe_ratio":               _safe_float(summary_json.get("PERatio")),
        "pe_fwd":                 _safe_float(summary_json.get("ForwardPE")),
        "peg_ratio":              _safe_float(summary_json.get("PEGRatio")),
        "ps_ttm_av":              _safe_float(summary_json.get("PriceToSalesRatioTTM")),
        "pb_ratio":               _safe_float(summary_json.get("PriceToBookRatio")),
        "ev_to_revenue_av":       _safe_float(summary_json.get("EVToRevenue")),
        "ev_to_ebitda_av":        _safe_float(summary_json.get("EVToEBITDA")),
        "dividend_yield":         _safe_float(summary_json.get("DividendYield")),
        "dividend_per_share":     _safe_float(summary_json.get("DividendPerShare")),
        "book_value_per_share":   _safe_float(summary_json.get("BookValue")),
        "diluted_eps_ttm":        _safe_float(summary_json.get("DilutedEPSTTM")),
        "revenue_per_share_ttm":  _safe_float(summary_json.get("RevenuePerShareTTM")),
        "profit_margin":          _safe_float(summary_json.get("ProfitMargin")),
        "operating_margin_ttm":   _safe_float(summary_json.get("OperatingMarginTTM")),
        "roa_ttm":                _safe_float(summary_json.get("ReturnOnAssetsTTM")),
        "roe_ttm":                _safe_float(summary_json.get("ReturnOnEquityTTM")),
        "rev_growth_yoy":         _safe_float(summary_json.get("QuarterlyRevenueGrowthYOY")),
        "eps_growth_yoy":         _safe_float(summary_json.get("QuarterlyEarningsGrowthYOY")),
        "beta":                   _safe_float(summary_json.get("Beta")),
        "week52_high":            _safe_float(summary_json.get("52WeekHigh")),
        "week52_low":             _safe_float(summary_json.get("52WeekLow")),
        "ma_50d":                 _safe_float(summary_json.get("50DayMovingAverage")),
        "ma_200d":                _safe_float(summary_json.get("200DayMovingAverage")),
        "analyst_target_price":   _safe_float(summary_json.get("AnalystTargetPrice")),
        "analyst_rating_strong_buy":  _safe_float(summary_json.get("AnalystRatingStrongBuy")),
        "analyst_rating_buy":         _safe_float(summary_json.get("AnalystRatingBuy")),
        "analyst_rating_hold":        _safe_float(summary_json.get("AnalystRatingHold")),
        "analyst_rating_sell":        _safe_float(summary_json.get("AnalystRatingSell")),
        "analyst_rating_strong_sell": _safe_float(summary_json.get("AnalystRatingStrongSell")),
    }

    # Cross-endpoint inputs for forward/cash-flow/dividend ratios
    try:
        fwd_eps, fwd_rev, fwd_eps_growth = forward_eps_and_revenue(symbol)
    except Exception:
        fwd_eps, fwd_rev, fwd_eps_growth = None, None, None
    try:
        ttm_div = ttm_dividend_sum(symbol)
    except Exception:
        ttm_div = 0.0

    income_rows: Optional[List[Dict[str, Any]]] = None
    try:
        income_rows = _with_av_retry(lambda: get_quarterly_statement_data(symbol))
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        income_rows = None

    try:
        cap = _with_av_retry(lambda: _build_cap_struct(symbol))
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        return []

    ttm = _build_ttm_table(symbol, income_rows)
    cf = _build_cashflow_ttm(symbol, income_rows)

    merged = cap.merge(ttm, on="fiscalDateEnding", how="left").merge(cf, on="fiscalDateEnding", how="left")
    merged = merged.sort_values("fiscalDateEnding", ascending=False).reset_index(drop=True)

    latest_price = float(merged["latest_closing_price"].iloc[0]) if not merged.empty else None
    latest_mc = float(merged["latestMC"].iloc[0]) if not merged.empty else None
    latest_ev = float(merged["latestEV"].iloc[0]) if not merged.empty else None
    latest_shares = float(merged["sharesOutstanding"].iloc[0]) if not merged.empty else None

    # Forward-looking ratios use the *current* price / EV — they are identical across all historical quarter rows.
    ev_to_sales_fwd = _safe_div(latest_ev, fwd_rev)
    ps_fwd = None
    if fwd_rev and latest_shares and latest_shares != 0:
        fwd_rev_per_share = fwd_rev / latest_shares
        ps_fwd = _safe_div(latest_price, fwd_rev_per_share)
    pe_fwd_nongaap = _safe_div(latest_price, fwd_eps)
    peg_nongaap_fwd = _safe_div(pe_fwd_nongaap, fwd_eps_growth) if fwd_eps_growth not in (None, 0) else None

    dividend_yield_ttm = _safe_div(ttm_div, latest_price) if ttm_div and latest_price else None

    now = datetime.now(timezone.utc)
    rows: List[Dict[str, Any]] = []

    for _, q in merged.iterrows():
        fiscal_date = q["fiscalDateEnding"].date() if pd.notna(q["fiscalDateEnding"]) else None
        if fiscal_date is None:
            continue

        mc = _safe_float(q.get("mc"))
        ev = _safe_float(q.get("ev"))
        price = _safe_float(q.get("adjustedPrice"))
        shares = _safe_float(q.get("sharesOutstanding"))
        rev_ttm = _safe_float(q.get("totalRevenue_ttm"))
        gross_ttm = _safe_float(q.get("grossProfit_ttm"))
        ebit_ttm = _safe_float(q.get("ebit_ttm"))
        ebitda_ttm = _safe_float(q.get("ebitda_ttm"))
        ni_ttm = _safe_float(q.get("netIncome_ttm"))
        ocf_ttm = _safe_float(q.get("operatingCashflow_ttm"))
        fcf_ttm = _safe_float(q.get("freeCashFlow_ttm"))
        div_payout_ttm = _safe_float(q.get("dividendPayout_ttm"))

        row: Dict[str, Any] = {
            "symbol":                  symbol,
            "fiscal_date_ending":      fiscal_date,
            "as_of_date":              now,
            "sector":                  sector,
            "industry":                industry,

            "shares_outstanding":      shares,
            "market_cap":              mc,
            "enterprise_value":        ev,
            "adjusted_price":          price,
            "latest_closing_price":    latest_price,
            "latest_market_cap":       latest_mc,
            "latest_enterprise_value": latest_ev,

            # Historical TTM multiples (quarter-specific)
            "ev_to_revenue":           _safe_div(ev, rev_ttm),
            "ev_to_gross_profit":      _safe_div(ev, gross_ttm),
            "ev_to_ebit":              _safe_div(ev, ebit_ttm),
            "ev_to_ebitda":            _safe_div(ev, ebitda_ttm),
            "ev_to_net_income":        _safe_div(ev, ni_ttm),
            "ev_to_fcf_ttm":           _safe_div(ev, fcf_ttm),
            "ps_ttm":                  _safe_div(mc, rev_ttm),
            "price_to_cash_flow_ttm":  _safe_div(mc, ocf_ttm),
            "price_to_fcf_ttm":        _safe_div(mc, fcf_ttm),
            "payout_ratio":            _safe_div(div_payout_ttm, ni_ttm),

            # Forward ratios (same for every row — derived from current price/EV × analyst estimates)
            "pe_fwd_nongaap":          pe_fwd_nongaap,
            "peg_nongaap_fwd":         peg_nongaap_fwd,
            "ev_to_sales_fwd":         ev_to_sales_fwd,
            "ps_fwd":                  ps_fwd,

            # Pass-through (AV OVERVIEW)
            "pe_ratio":                av_ratios["pe_ratio"],
            "pe_fwd":                  av_ratios["pe_fwd"],
            "peg_ratio":               av_ratios["peg_ratio"],
            "pb_ratio":                av_ratios["pb_ratio"],
            "dividend_yield":          av_ratios["dividend_yield"],
            "dividend_yield_ttm":      dividend_yield_ttm,
            "dividend_per_share":      av_ratios["dividend_per_share"],
            "profit_margin":           av_ratios["profit_margin"],
            "operating_margin_ttm":    av_ratios["operating_margin_ttm"],
            "roa_ttm":                 av_ratios["roa_ttm"],
            "roe_ttm":                 av_ratios["roe_ttm"],
            "book_value_per_share":    av_ratios["book_value_per_share"],
            "diluted_eps_ttm":         av_ratios["diluted_eps_ttm"],
            "revenue_per_share_ttm":   av_ratios["revenue_per_share_ttm"],
            "rev_growth_yoy":          av_ratios["rev_growth_yoy"],
            "eps_growth_yoy":          av_ratios["eps_growth_yoy"],
            "beta":                    av_ratios["beta"],
            "week52_high":             av_ratios["week52_high"],
            "week52_low":              av_ratios["week52_low"],
            "ma_50d":                  av_ratios["ma_50d"],
            "ma_200d":                 av_ratios["ma_200d"],
            "analyst_target_price":    av_ratios["analyst_target_price"],
            "analyst_rating_strong_buy":  _int_or_none(av_ratios["analyst_rating_strong_buy"]),
            "analyst_rating_buy":         _int_or_none(av_ratios["analyst_rating_buy"]),
            "analyst_rating_hold":        _int_or_none(av_ratios["analyst_rating_hold"]),
            "analyst_rating_sell":        _int_or_none(av_ratios["analyst_rating_sell"]),
            "analyst_rating_strong_sell": _int_or_none(av_ratios["analyst_rating_strong_sell"]),
        }
        rows.append(row)

    return rows


def _int_or_none(v: Optional[float]) -> Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _serialize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Make a snapshot row JSON-friendly (dates -> ISO, Decimal -> float)."""
    out: Dict[str, Any] = {}
    for k, v in row.items():
        if hasattr(v, "isoformat"):
            out[k] = v.isoformat()
        elif isinstance(v, (int, float)) or v is None:
            out[k] = v
        else:
            # asyncpg may return Decimal; cast to float for JSON
            try:
                out[k] = float(v)
            except (TypeError, ValueError):
                out[k] = v
    # Back-compat aliases for frontend consumers that still use camelCase keys
    out["fiscalDateEnding"] = out.get("fiscal_date_ending")
    out["symbol"] = out.get("symbol")
    return out


async def _get_or_refresh(symbol: str) -> List[Dict[str, Any]]:
    """Prefer Postgres snapshots when ``DATABASE_URL`` is set; refresh from AV only when stale.

    If a refresh fails (e.g. rate limit) but cached rows exist, returns the cache (stale-while-revalidate).
    """
    started_at = time.perf_counter()
    pool = await db.get_pool()
    if pool is None:
        rows = await asyncio.get_event_loop().run_in_executor(None, _compute_snapshot_rows, symbol)
        logger.info(
            "valuation_refresh symbol=%s source=direct rows=%d ms=%.1f",
            symbol,
            len(rows),
            (time.perf_counter() - started_at) * 1000,
        )
        return rows

    cached_rows = await db.fetch_snapshots(symbol)
    latest = cached_rows[0] if cached_rows else None

    if cached_rows and not db.is_stale(latest):
        logger.info(
            "valuation_refresh symbol=%s source=cache rows=%d ms=%.1f",
            symbol,
            len(cached_rows),
            (time.perf_counter() - started_at) * 1000,
        )
        return cached_rows

    try:
        rows = await db.run_singleflight(
            f"valuation_snapshot_refresh:{symbol}",
            lambda: asyncio.get_event_loop().run_in_executor(None, _compute_snapshot_rows, symbol),
        )
    except HTTPException as exc:
        if cached_rows:
            logger.warning(
                "Valuation refresh failed for %s; serving %d cached row(s). detail=%s",
                symbol,
                len(cached_rows),
                exc.detail,
            )
            logger.info(
                "valuation_refresh symbol=%s source=stale_cache rows=%d ms=%.1f",
                symbol,
                len(cached_rows),
                (time.perf_counter() - started_at) * 1000,
            )
            return cached_rows
        raise

    if rows:
        await db.upsert_snapshots(rows)
        await db.refresh_5y_avg(symbol)
        fresh = await db.fetch_snapshots(symbol)
        out = fresh or rows
        logger.info(
            "valuation_refresh symbol=%s source=refresh rows=%d ms=%.1f",
            symbol,
            len(out),
            (time.perf_counter() - started_at) * 1000,
        )
        return out
    if cached_rows:
        logger.warning(
            "Valuation refresh produced no rows for %s; serving %d cached row(s)",
            symbol,
            len(cached_rows),
        )
        logger.info(
            "valuation_refresh symbol=%s source=empty_stale rows=%d ms=%.1f",
            symbol,
            len(cached_rows),
            (time.perf_counter() - started_at) * 1000,
        )
        return cached_rows
    logger.info(
        "valuation_refresh symbol=%s source=empty rows=0 ms=%.1f",
        symbol,
        (time.perf_counter() - started_at) * 1000,
    )
    return []


# ---------- routes ----------

@router.get("/valuation/quarterly/{ticker}/ttm")
async def get_valuation(ticker: str):
    """Primary endpoint consumed by the frontend. Returns all snapshot rows newest-first."""
    symbol = (ticker or "").strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Missing ticker")
    try:
        rows = await _get_or_refresh(symbol)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        # AV upstream / transient compute failures should not blow up the page.
        # Log full traceback so the underlying cause is visible in the server console.
        logger.exception("Valuation TTM refresh failed for %s; serving empty payload.", symbol)
        return []
    except Exception:
        logger.exception("Valuation TTM unexpected failure for %s; serving empty payload.", symbol)
        return []
    return [_serialize_row(r) for r in rows]


@router.get("/valuation/quarterly/{ticker}")
def calculate_valuations(ticker: str):
    """Back-compat shim: the old endpoint returned per-quarter TTM fundamentals.

    Preserved so existing callers keep working. Prefer `/valuation/quarterly/{ticker}/ttm`.
    """
    ttm = _build_ttm_table(ticker)
    if ttm.empty:
        return []
    out = ttm.copy()
    out["fiscalDateEnding"] = out["fiscalDateEnding"].dt.strftime("%Y-%m-%d")
    for col in out.columns:
        if col != "fiscalDateEnding":
            out[col] = out[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0")
    return out.to_dict(orient="records")


@router.get("/valuation/layout/{ticker}")
async def get_valuation_layout(ticker: str):
    """Returns the sector-ordered list of ratios + the latest row's values.

    Response shape:
        {
            "symbol": "IOT",
            "sector": "TECHNOLOGY",
            "industry": "SOFTWARE - INFRASTRUCTURE",
            "order": ["ps_fwd", "ps_ttm", ...],
            "labels": {"ps_fwd": "P/S (FWD)", ...},
            "values": {"ps_fwd": 9.02, ...},
            "five_year_avg": {"ps_ttm_5y": 15.96, ...},
        }
    """
    symbol = (ticker or "").strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Missing ticker")

    rows: List[Dict[str, Any]] = []
    try:
        rows = await _get_or_refresh(symbol)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Valuation layout refresh failed for %s; serving empty layout.", symbol)
    except Exception:
        logger.exception("Valuation layout unexpected failure for %s; serving empty layout.", symbol)

    if not rows:
        return {
            "symbol": symbol,
            "sector": None,
            "industry": None,
            "order": [],
            "labels": {},
            "values": {},
            "latest": {},
            "five_year_avg": {},
        }

    latest = rows[0]
    order = get_ratio_priority(latest.get("sector"))
    try:
        five_y = await db.fetch_5y_avg(symbol) or {}
    except Exception as exc:
        logger.warning("Failed reading 5Y valuation cache for %s; continuing without it. detail=%s", symbol, exc)
        five_y = {}

    serialized_latest = _serialize_row(latest)
    values = {col: serialized_latest.get(col) for col in order}
    five_y_out = {k: (float(v) if v is not None else None) for k, v in five_y.items() if k != "symbol" and k != "computed_at"}

    return {
        "symbol": symbol,
        "sector": latest.get("sector"),
        "industry": latest.get("industry"),
        "order": order,
        "labels": {col: label_for(col) for col in order},
        "values": values,
        "latest": serialized_latest,
        "five_year_avg": five_y_out,
    }


# Exposed for other modules (e.g. summary.py news ttm_display)
async def get_valuation_async(ticker: str) -> List[Dict[str, Any]]:
    symbol = (ticker or "").strip().upper()
    return [_serialize_row(r) for r in await _get_or_refresh(symbol)]
