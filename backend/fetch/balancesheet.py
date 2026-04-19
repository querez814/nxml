from fastapi import APIRouter, HTTPException
from fetch.av_util import av_get_json_sync
import requests as r
import dotenv as env
import os
import asyncio
import logging
import pandas as pd
import numpy as np
from typing import Any, Dict, List

import db

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()
logger = logging.getLogger(__name__)


def _compute_quarterly_balance_sheet_from_av(ticker: str) -> List[Dict[str, Any]]:
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={av_api}"
    data_json = av_get_json_sync(url)
    quarterly_reports = data_json.get("quarterlyReports", [])
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly balance sheet data found")

    df = pd.DataFrame(quarterly_reports)
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)
    if "totalCurrentAssets" in df.columns and "totalCurrentLiabilities" in df.columns:
        df["working_capital"] = df["totalCurrentAssets"] - df["totalCurrentLiabilities"]
    else:
        df["working_capital"] = 0

    df["current_ratio"] = df["totalCurrentAssets"] / df["totalCurrentLiabilities"]
    df["quick_ratio"] = (df["totalCurrentAssets"] - df["inventory"]) / df["totalCurrentLiabilities"]
    df["cash_ratio"] = df["cashAndCashEquivalentsAtCarryingValue"] / df["totalCurrentLiabilities"]
    df["debt_to_equity_ratio"] = df["totalLiabilities"] / df["totalShareholderEquity"]
    df["debt_to_asset_ratio"] = df["totalLiabilities"] / df["totalAssets"]
    df["book_value_per_share"] = df["totalShareholderEquity"] / df["commonStockSharesOutstanding"]

    keys_to_include = [
        "fiscalDateEnding", "totalCurrentAssets", "totalAssets", "totalCurrentLiabilities",
        "totalLiabilities", "working_capital", "totalShareholderEquity",
        "commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "inventory",
        "propertyPlantEquipment", "deferredRevenue", "currentDebt", "current_ratio",
        "quick_ratio", "cash_ratio", "debt_to_equity_ratio", "debt_to_asset_ratio",
        "book_value_per_share"
    ]

    result_df = df[keys_to_include] if set(keys_to_include).issubset(df.columns) else df
    result_df = result_df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col != "fiscalDateEnding"]

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]

    for col in numeric_cols:
        if col in [
            "current_ratio", "quick_ratio", "cash_ratio",
            "debt_to_equity_ratio", "debt_to_asset_ratio",
            "book_value_per_share"
        ]:
            result_df[col] = result_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")
            temp_series = pd.to_numeric(result_df[col], errors='coerce')
        else:
            temp_series = result_df[col]

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
    return final_df.to_dict(orient="records")


async def fetch_balance_quarterly_cached(ticker: str) -> List[Dict[str, Any]]:
    sym = (ticker or "").strip().upper()
    if not sym:
        raise HTTPException(status_code=400, detail="Missing ticker")

    cached = await db.fetch_financial_cache_row(sym, db.DATASET_BALANCE_QUARTERLY)
    if cached and not db.is_financial_cache_row_stale(cached):
        return cached["payload"]

    try:
        rows = await db.run_singleflight(
            f"balance_quarterly_refresh:{sym}",
            lambda: asyncio.to_thread(_compute_quarterly_balance_sheet_from_av, sym),
        )
    except HTTPException as exc:
        if cached and cached.get("payload") is not None:
            logger.warning(
                "Balance quarterly AV refresh failed for %s; serving stale cache. detail=%s",
                sym,
                getattr(exc, "detail", exc),
            )
            return list(cached["payload"])
        raise

    if rows:
        lf = db.latest_fiscal_date_from_statement_rows(rows)
        await db.upsert_financial_cache(sym, db.DATASET_BALANCE_QUARTERLY, rows, lf)
    return rows


def get_quarterly_balance_sheet_data(ticker: str) -> List[Dict[str, Any]]:
    return db.sync_wait_awaitable(lambda: fetch_balance_quarterly_cached(ticker))


@router.get("/balancesheet-statement/quarterly/{ticker}")
async def read_quarterly_balance_sheet(ticker: str):
    try:
        return await fetch_balance_quarterly_cached(ticker)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Balance quarterly request failed for %s; serving empty list.", ticker)
        return []
    except Exception:
        logger.exception("Balance quarterly unexpected failure for %s; serving empty list.", ticker)
        return []


def _compute_annual_balance_sheet_from_av(ticker: str) -> List[Dict[str, Any]]:
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={av_api}"
    data_json = av_get_json_sync(url)
    annual_reports = data_json.get("annualReports", [])
    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly balance sheet data found")

    df = pd.DataFrame(annual_reports)
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)
    if "totalCurrentAssets" in df.columns and "totalCurrentLiabilities" in df.columns:
        df["working_capital"] = df["totalCurrentAssets"] - df["totalCurrentLiabilities"]
    else:
        df["working_capital"] = 0

    df["current_ratio"] = df["totalCurrentAssets"] / df["totalCurrentLiabilities"]
    df["quick_ratio"] = (df["totalCurrentAssets"] - df["inventory"]) / df["totalCurrentLiabilities"]
    df["cash_ratio"] = df["cashAndCashEquivalentsAtCarryingValue"] / df["totalCurrentLiabilities"]
    df["debt_to_equity_ratio"] = df["totalLiabilities"] / df["totalShareholderEquity"]
    df["debt_to_asset_ratio"] = df["totalLiabilities"] / df["totalAssets"]
    df["book_value_per_share"] = df["totalShareholderEquity"] / df["commonStockSharesOutstanding"]

    keys_to_include = [
        "fiscalDateEnding", "totalCurrentAssets", "totalAssets", "totalCurrentLiabilities",
        "totalLiabilities", "working_capital", "totalShareholderEquity",
        "commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "inventory",
        "propertyPlantEquipment", "deferredRevenue", "currentDebt", "current_ratio",
        "quick_ratio", "cash_ratio", "debt_to_equity_ratio", "debt_to_asset_ratio",
        "book_value_per_share"
    ]

    result_df = df[keys_to_include] if set(keys_to_include).issubset(df.columns) else df
    result_df = result_df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col != "fiscalDateEnding"]

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]

    for col in numeric_cols:
        if col in [
            "current_ratio", "quick_ratio", "cash_ratio",
            "debt_to_equity_ratio", "debt_to_asset_ratio",
            "book_value_per_share"
        ]:
            result_df[col] = result_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")
            temp_series = pd.to_numeric(result_df[col], errors='coerce')
        else:
            temp_series = result_df[col]

        prev_1 = temp_series.shift(1)
        yoy_series = ((temp_series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")


async def fetch_balance_annual_cached(ticker: str) -> List[Dict[str, Any]]:
    sym = (ticker or "").strip().upper()
    if not sym:
        raise HTTPException(status_code=400, detail="Missing ticker")

    cached = await db.fetch_financial_cache_row(sym, db.DATASET_BALANCE_ANNUAL)
    if cached and not db.is_financial_cache_row_stale(cached):
        return cached["payload"]

    try:
        rows = await db.run_singleflight(
            f"balance_annual_refresh:{sym}",
            lambda: asyncio.to_thread(_compute_annual_balance_sheet_from_av, sym),
        )
    except HTTPException as exc:
        if cached and cached.get("payload") is not None:
            logger.warning(
                "Balance annual AV refresh failed for %s; serving stale cache. detail=%s",
                sym,
                getattr(exc, "detail", exc),
            )
            return list(cached["payload"])
        raise

    if rows:
        lf = db.latest_fiscal_date_from_statement_rows(rows)
        await db.upsert_financial_cache(sym, db.DATASET_BALANCE_ANNUAL, rows, lf)
    return rows


def get_annual_balance_sheet_data(ticker: str) -> List[Dict[str, Any]]:
    return db.sync_wait_awaitable(lambda: fetch_balance_annual_cached(ticker))


@router.get("/balancesheet-statement/annual/{ticker}")
async def read_annual_balance_sheet(ticker: str):
    try:
        return await fetch_balance_annual_cached(ticker)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Balance annual request failed for %s; serving empty list.", ticker)
        return []
    except Exception:
        logger.exception("Balance annual unexpected failure for %s; serving empty list.", ticker)
        return []
