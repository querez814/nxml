import math
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fetch.av_util import av_get_json_sync
from fetch.income_statement import fetch_income_quarterly_cached, fetch_income_annual_cached
import requests as r
import dotenv as env
import os
import asyncio
import logging
import pandas as pd
import numpy as np

import db

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()
logger = logging.getLogger(__name__)


def _sanitize_json_value(value: Any) -> Any:
    """Starlette's json.dumps rejects float nan/inf; normalize for API responses and cache writes."""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, (np.floating, np.integer)):
        try:
            inner = value.item()
        except Exception:
            return value
        if isinstance(inner, float) and (math.isnan(inner) or math.isinf(inner)):
            return None
        return inner
    return value


def _sanitize_records_for_json(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{k: _sanitize_json_value(v) for k, v in row.items()} for row in records]


def _revenue_denominator(df: pd.DataFrame) -> pd.Series:
    """
    After merging income, revenue may be `totalRevenue` (no name clash) or `totalRevenue_income`.
    Using the wrong name left the series as NaN and forced OCF/FCF margins to 0%.
    """
    if "totalRevenue_income" in df.columns:
        rev = pd.to_numeric(df["totalRevenue_income"], errors="coerce")
    elif "totalRevenue" in df.columns:
        rev = pd.to_numeric(df["totalRevenue"], errors="coerce")
    else:
        rev = pd.Series(np.nan, index=df.index, dtype="float64")
    return rev.replace(0, np.nan)


def _normalize_income_records(raw: Optional[Any]) -> List[Dict[str, Any]]:
    """Best-effort normalize income payloads into a list of row dicts."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return [row for row in raw if isinstance(row, dict)]
    if isinstance(raw, dict):
        rows = raw.get("rows")
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
        return [raw]
    logger.warning("Unexpected income payload type for cashflow compute: %s", type(raw).__name__)
    return []


def _compute_quarterly_cashflow_from_av(
    ticker: str, income_records: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={av_api}"
    data_json = av_get_json_sync(url)
    quarterly_reports = data_json.get("quarterlyReports", [])
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly cash flow data found")

    df = pd.DataFrame(quarterly_reports)
    income_df = pd.DataFrame(_normalize_income_records(income_records))

    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in income_df.columns:
        if col != "fiscalDateEnding":
            income_df[col] = pd.to_numeric(income_df[col], errors='coerce')

    df["freeCashFlow"] = df["operatingCashflow"] - df["capitalExpenditures"]

    df.replace([np.inf, -np.inf, pd.NA], 0, inplace=True)
    df.fillna(0, inplace=True)

    keys_to_exclude = [
        "reportedCurrency",
        "proceedsFromIssuanceOfCommonStock",
        "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
        "proceedsFromIssuanceOfPreferredStock",
        "proceedsFromSaleOfTreasuryStock",
        "changeInCashAndCashEquivalents",
        "changeInExchangeRate"
    ]
    df = df.drop(columns=keys_to_exclude, errors='ignore')

    if not income_df.empty and "totalRevenue" in income_df.columns:
        if "fiscalDateEnding" in income_df.columns:
            income_rev = income_df[["fiscalDateEnding", "totalRevenue"]].copy()
            income_rev["totalRevenue"] = pd.to_numeric(income_rev["totalRevenue"], errors="coerce")
            df = df.merge(income_rev, on="fiscalDateEnding", how="left", suffixes=("", "_income"))
        else:
            df["totalRevenue"] = pd.to_numeric(income_df["totalRevenue"], errors="coerce").reindex(
                df.index
            )
    revenue_denom = _revenue_denominator(df)

    df["net_profit_margin"] = (df["netIncome"] / df["operatingCashflow"]) * 100
    df["ocf_margin"] = (df["operatingCashflow"] / revenue_denom) * 100
    df["fcf_margin"] = (df["freeCashFlow"] / revenue_denom) * 100

    df["roce"] = df["netIncome"] / df["capitalExpenditures"]
    df["cash_flow_adequacy_ratio"] = df["operatingCashflow"] / (
        df["capitalExpenditures"] + df["dividendPayout"] + df["cashflowFromFinancing"]
    )
    df["capex_ratio"] = df["operatingCashflow"] / df["capitalExpenditures"]
    df["change_working_capital"] = df["changeInReceivables"] - df["changeInInventory"]

    ratio_cols = ["roce", "cash_flow_adequacy_ratio", "capex_ratio", "change_working_capital"]
    for col in ratio_cols:
        df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")

    margin_cols = ["net_profit_margin", "ocf_margin", "fcf_margin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [c for c in result_df.columns if c not in ["fiscalDateEnding"] + margin_cols + ratio_cols]

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]

    for col in numeric_cols:
        prev_4 = result_df[col].shift(4)
        prev_1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev_4) / prev_4.abs()) * 100
        qoq_series = ((result_df[col] - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        qoq_series = qoq_series.replace([np.inf, -np.inf], 0).fillna(0)

        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        change_df[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    for col in margin_cols + ratio_cols:
        temp_series = pd.to_numeric(result_df[col].str.replace("%", ""), errors='coerce')
        prev_4 = temp_series.shift(4)
        prev_1 = temp_series.shift(1)
        yoy_series = ((temp_series - prev_4) / prev_4.abs()) * 100
        qoq_series = ((temp_series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        qoq_series = qoq_series.replace([np.inf, -np.inf], 0).fillna(0)

        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        change_df[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return _sanitize_records_for_json(final_df.to_dict(orient="records"))


async def fetch_cashflow_quarterly_cached(
    ticker: str, income_records: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    sym = (ticker or "").strip().upper()
    if not sym:
        raise HTTPException(status_code=400, detail="Missing ticker")

    # Caller-supplied income rows (e.g. valuation pipeline): compute only, no cache read/write.
    if income_records is not None:
        normalized_income = _normalize_income_records(income_records)
        return await asyncio.to_thread(_compute_quarterly_cashflow_from_av, sym, normalized_income)

    cached = await db.fetch_financial_cache_row(sym, db.DATASET_CASHFLOW_QUARTERLY)
    if cached and not db.is_financial_cache_row_stale(cached):
        return _sanitize_records_for_json(list(cached["payload"]))

    if income_records is None:
        income_records = _normalize_income_records(await fetch_income_quarterly_cached(sym))

    try:
        rows = await db.run_singleflight(
            f"cashflow_quarterly_refresh:{sym}",
            lambda: asyncio.to_thread(_compute_quarterly_cashflow_from_av, sym, income_records),
        )
    except HTTPException as exc:
        if cached and cached.get("payload") is not None:
            logger.warning(
                "Cashflow quarterly AV refresh failed for %s; serving stale cache. detail=%s",
                sym,
                getattr(exc, "detail", exc),
            )
            return _sanitize_records_for_json(list(cached["payload"]))
        raise

    if rows:
        lf = db.latest_fiscal_date_from_statement_rows(rows)
        await db.upsert_financial_cache(sym, db.DATASET_CASHFLOW_QUARTERLY, rows, lf)
    return _sanitize_records_for_json(rows)


def get_quarterly_cashflow_statement_data(
    ticker: str, income_records: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    return db.sync_wait_awaitable(lambda: fetch_cashflow_quarterly_cached(ticker, income_records))


@router.get("/cashflow-statement/quarterly/{ticker}")
async def read_quarterly_cashflow(ticker: str):
    try:
        return await fetch_cashflow_quarterly_cached(ticker, None)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Cashflow quarterly request failed for %s; serving empty list.", ticker)
        return []
    except Exception:
        logger.exception("Cashflow quarterly unexpected failure for %s; serving empty list.", ticker)
        return []


def _compute_annual_cashflow_from_av(
    ticker: str, income_annual: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={av_api}"
    data_json = av_get_json_sync(url)
    annual_reports = data_json.get("annualReports", [])
    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly cash flow data found")

    df = pd.DataFrame(annual_reports)
    income_df = pd.DataFrame(_normalize_income_records(income_annual))

    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in income_df.columns:
        if col != "fiscalDateEnding":
            income_df[col] = pd.to_numeric(income_df[col], errors='coerce')

    df["freeCashFlow"] = df["operatingCashflow"] - df["capitalExpenditures"]

    df.replace([np.inf, -np.inf, pd.NA], 0, inplace=True)
    df.fillna(0, inplace=True)

    keys_to_exclude = [
        "reportedCurrency",
        "proceedsFromIssuanceOfCommonStock",
        "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
        "proceedsFromIssuanceOfPreferredStock",
        "proceedsFromSaleOfTreasuryStock",
        "changeInCashAndCashEquivalents",
        "changeInExchangeRate"
    ]
    df = df.drop(columns=keys_to_exclude, errors='ignore')

    if not income_df.empty and "totalRevenue" in income_df.columns:
        if "fiscalDateEnding" in income_df.columns:
            income_rev = income_df[["fiscalDateEnding", "totalRevenue"]].copy()
            income_rev["totalRevenue"] = pd.to_numeric(income_rev["totalRevenue"], errors="coerce")
            df = df.merge(income_rev, on="fiscalDateEnding", how="left", suffixes=("", "_income"))
        else:
            df["totalRevenue"] = pd.to_numeric(income_df["totalRevenue"], errors="coerce").reindex(
                df.index
            )
    revenue_denom = _revenue_denominator(df)

    df["net_profit_margin"] = (df["netIncome"] / df["operatingCashflow"]) * 100
    df["ocf_margin"] = (df["operatingCashflow"] / revenue_denom) * 100
    df["fcf_margin"] = (df["freeCashFlow"] / revenue_denom) * 100

    df["roce"] = df["netIncome"] / df["capitalExpenditures"]
    df["cash_flow_adequacy_ratio"] = df["operatingCashflow"] / (
        df["capitalExpenditures"] + df["dividendPayout"] + df["cashflowFromFinancing"]
    )
    df["capex_ratio"] = df["operatingCashflow"] / df["capitalExpenditures"]
    df["change_working_capital"] = df["changeInReceivables"] - df["changeInInventory"]

    ratio_cols = ["roce", "cash_flow_adequacy_ratio", "capex_ratio", "change_working_capital"]
    for col in ratio_cols:
        df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")

    margin_cols = ["net_profit_margin", "ocf_margin", "fcf_margin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [c for c in result_df.columns if c not in ["fiscalDateEnding"] + margin_cols + ratio_cols]

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]

    for col in numeric_cols:
        prev_1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    for col in margin_cols + ratio_cols:
        temp_series = pd.to_numeric(result_df[col].str.replace("%", ""), errors='coerce')
        prev_1 = temp_series.shift(1)
        yoy_series = ((temp_series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return _sanitize_records_for_json(final_df.to_dict(orient="records"))


async def fetch_cashflow_annual_cached(ticker: str) -> List[Dict[str, Any]]:
    sym = (ticker or "").strip().upper()
    if not sym:
        raise HTTPException(status_code=400, detail="Missing ticker")

    cached = await db.fetch_financial_cache_row(sym, db.DATASET_CASHFLOW_ANNUAL)
    if cached and not db.is_financial_cache_row_stale(cached):
        return _sanitize_records_for_json(list(cached["payload"]))

    income_annual = await fetch_income_annual_cached(sym)

    try:
        rows = await db.run_singleflight(
            f"cashflow_annual_refresh:{sym}",
            lambda: asyncio.to_thread(_compute_annual_cashflow_from_av, sym, income_annual),
        )
    except HTTPException as exc:
        if cached and cached.get("payload") is not None:
            logger.warning(
                "Cashflow annual AV refresh failed for %s; serving stale cache. detail=%s",
                sym,
                getattr(exc, "detail", exc),
            )
            return _sanitize_records_for_json(list(cached["payload"]))
        raise

    if rows:
        lf = db.latest_fiscal_date_from_statement_rows(rows)
        await db.upsert_financial_cache(sym, db.DATASET_CASHFLOW_ANNUAL, rows, lf)
    return _sanitize_records_for_json(rows)


def get_annual_cashflow_statement_data(ticker: str) -> List[Dict[str, Any]]:
    return db.sync_wait_awaitable(lambda: fetch_cashflow_annual_cached(ticker))


@router.get("/cashflow-statement/annual/{ticker}")
async def read_annual_cashflow(ticker: str):
    try:
        return await fetch_cashflow_annual_cached(ticker)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Cashflow annual request failed for %s; serving empty list.", ticker)
        return []
    except Exception:
        logger.exception("Cashflow annual unexpected failure for %s; serving empty list.", ticker)
        return []
