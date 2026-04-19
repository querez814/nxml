
from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import asyncio
import logging
import pandas as pd
import numpy as np
import gc
from typing import Any, Dict, List, Optional

from fetch.av_util import av_get_json_sync
from fetch.earnings import get_quarterly_earnings_data as earnings
import db

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()
logger = logging.getLogger(__name__)


def calculate_changes(df: pd.DataFrame, col: str, is_margin: bool = False) -> Dict:
    temp_dict = {"fiscalDateEnding": df["fiscalDateEnding"]}

    if is_margin:
        series = pd.to_numeric(df[col].str.replace('%', ''), errors='coerce')
    else:
        series = df[col]

    prev4 = series.shift(4)
    prev1 = series.shift(1)

    # Calculate YoY and QoQ changes
    yoy = ((series - prev4) / prev4.abs()) * 100
    qoq = ((series - prev1) / prev1.abs()) * 100

    # Calculate derivatives
    yoy_deriv = ((yoy - yoy.shift(1)) / yoy.shift(1).abs()) * 100
    qoq_deriv = ((qoq - qoq.shift(1)) / qoq.shift(1).abs()) * 100

    # Format results
    temp_dict.update({
        f"{col}_YoY": yoy.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%"),
        f"{col}_QoQ": qoq.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%"),
        f"{col}_YoY_Derivative": yoy_deriv.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%"),
        f"{col}_QoQ_Derivative": qoq_deriv.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    })

    return temp_dict


def _compute_quarterly_statement_data_from_av(ticker: str) -> List[Dict[str, Any]]:
    data_json = av_get_json_sync(
        f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={av_api}"
    )
    quarterly_reports = data_json.get("quarterlyReports", [])
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly reports found")

    try:
        df = pd.DataFrame(quarterly_reports)
        earnings_df = pd.DataFrame(earnings(ticker))

        for col in df.columns:
            if col != "fiscalDateEnding":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]:
            earnings_df[col] = pd.to_numeric(earnings_df[col], errors='coerce')

        df = df.replace([np.inf, -np.inf, np.nan], 0)
        earnings_df = earnings_df.replace([np.inf, -np.inf, np.nan], 0)

        for col in ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]:
            df[col] = earnings_df[col]

        keys_to_exclude = [
            'reportedCurrency', 'investmentIncomeNet', 'netInterestIncome',
            'nonInterestIncome', 'otherNonOperatingIncome', 'depreciation',
            'depreciationAndAmortization', 'netIncomeFromContinuingOperations',
            'comprehensiveIncomeNetOfTax'
        ]
        df = df.drop(columns=keys_to_exclude, errors='ignore')

        margins = {
            "grossMargin": ("grossProfit", "totalRevenue"),
            "operatingMargin": ("operatingIncome", "totalRevenue"),
            "ebitMargin": ("ebit", "totalRevenue"),
            "ebitdaMargin": ("ebitda", "totalRevenue"),
            "netMargin": ("netIncome", "totalRevenue")
        }

        for margin, (num, denom) in margins.items():
            df[margin] = (df[num] / df[denom]) * 100
            df[margin] = df[margin].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

        result_df = df.iloc[::-1].reset_index(drop=True)
        margin_cols = list(margins.keys())
        numeric_cols = [col for col in result_df.columns if col not in ["fiscalDateEnding"] + margin_cols]

        changes_dfs = []
        chunk_size = 5

        for i in range(0, len(numeric_cols), chunk_size):
            chunk = numeric_cols[i:i + chunk_size]
            for col in chunk:
                changes = calculate_changes(result_df, col)
                changes_dfs.append(pd.DataFrame(changes))
                del changes
                gc.collect()

        for col in margin_cols:
            changes = calculate_changes(result_df, col, is_margin=True)
            changes_dfs.append(pd.DataFrame(changes))
            del changes
            gc.collect()

        all_changes = changes_dfs[0]
        for df_change in changes_dfs[1:]:
            all_changes = pd.merge(all_changes, df_change, on="fiscalDateEnding")
            del df_change
            gc.collect()

        final_df = pd.merge(result_df, all_changes, on="fiscalDateEnding")
        final_df = final_df.iloc[::-1].reset_index(drop=True)
        final_df = final_df.replace([np.inf, -np.inf, np.nan], 0)

        del result_df, all_changes, changes_dfs
        gc.collect()

        return final_df.to_dict(orient="records")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def fetch_income_quarterly_cached(ticker: str) -> List[Dict[str, Any]]:
    sym = (ticker or "").strip().upper()
    if not sym:
        raise HTTPException(status_code=400, detail="Missing ticker")

    cached = await db.fetch_financial_cache_row(sym, db.DATASET_INCOME_QUARTERLY)
    if cached and not db.is_financial_cache_row_stale(cached):
        return cached["payload"]

    try:
        rows = await db.run_singleflight(
            f"income_quarterly_refresh:{sym}",
            lambda: asyncio.to_thread(_compute_quarterly_statement_data_from_av, sym),
        )
    except HTTPException as exc:
        if cached and cached.get("payload") is not None:
            logger.warning(
                "Income quarterly AV refresh failed for %s; serving stale cache. detail=%s",
                sym,
                getattr(exc, "detail", exc),
            )
            return list(cached["payload"])
        raise

    if rows:
        lf = db.latest_fiscal_date_from_statement_rows(rows)
        await db.upsert_financial_cache(sym, db.DATASET_INCOME_QUARTERLY, rows, lf)
    return rows


def get_quarterly_statement_data(ticker: str) -> List[Dict[str, Any]]:
    return db.sync_wait_awaitable(lambda: fetch_income_quarterly_cached(ticker))


@router.get("/income-statement/quarterly/{ticker}")
async def read_quarterly_income_statement(ticker: str):
    try:
        return await fetch_income_quarterly_cached(ticker)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Income quarterly request failed for %s; serving empty list.", ticker)
        return []
    except Exception:
        logger.exception("Income quarterly unexpected failure for %s; serving empty list.", ticker)
        return []


def _compute_annual_statement_data_from_av(ticker: str) -> List[Dict[str, Any]]:
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={av_api}"
    data_json = av_get_json_sync(url)
    annual_reports = data_json.get("annualReports", [])
    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly reports found.")
    df = pd.DataFrame(annual_reports)
    earnings_df = pd.DataFrame(earnings(ticker))
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]:
        earnings_df[col] = pd.to_numeric(earnings_df[col], errors='coerce')
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)
    earnings_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    earnings_df.fillna(0, inplace=True)
    df["reportedEPS"] = earnings_df["reportedEPS"]
    df["estimatedEPS"] = earnings_df["estimatedEPS"]
    df["surprise"] = earnings_df["surprise"]
    df["surprisePercentage"] = earnings_df["surprisePercentage"]
    keys_to_exclude = [
        'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]
    df = df.drop(columns=keys_to_exclude, errors='ignore')
    df["grossMargin"] = (df["grossProfit"] / df["totalRevenue"]) * 100
    df["operatingMargin"] = (df["operatingIncome"] / df["totalRevenue"]) * 100
    df["ebitMargin"] = (df["ebit"] / df["totalRevenue"]) * 100
    df["ebitdaMargin"] = (df["ebitda"] / df["totalRevenue"]) * 100
    df["netMargin"] = (df["netIncome"] / df["totalRevenue"]) * 100
    margin_cols = ["grossMargin", "operatingMargin", "ebitMargin", "ebitdaMargin", "netMargin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col not in ["fiscalDateEnding"] + margin_cols]
    changes_list = []
    for col in numeric_cols:
        temp_dict = {"fiscalDateEnding": result_df["fiscalDateEnding"]}
        prev1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev1) / prev1.abs()) * 100
        temp_dict[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        changes_list.append(pd.DataFrame(temp_dict))
    for col in margin_cols:
        temp_dict = {"fiscalDateEnding": result_df["fiscalDateEnding"]}
        numeric_margin = pd.to_numeric(result_df[col].str.replace('%', ''), errors='coerce')
        prev1_margin = numeric_margin.shift(1)
        yoy_series = ((numeric_margin - prev1_margin) / prev1_margin.abs()) * 100
        temp_dict[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        changes_list.append(pd.DataFrame(temp_dict))
    all_changes = changes_list[0]
    for df_change in changes_list[1:]:
        all_changes = pd.merge(all_changes, df_change, on="fiscalDateEnding")
    final_df = pd.merge(result_df, all_changes, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")


async def fetch_income_annual_cached(ticker: str) -> List[Dict[str, Any]]:
    sym = (ticker or "").strip().upper()
    if not sym:
        raise HTTPException(status_code=400, detail="Missing ticker")

    cached = await db.fetch_financial_cache_row(sym, db.DATASET_INCOME_ANNUAL)
    if cached and not db.is_financial_cache_row_stale(cached):
        return cached["payload"]

    try:
        rows = await db.run_singleflight(
            f"income_annual_refresh:{sym}",
            lambda: asyncio.to_thread(_compute_annual_statement_data_from_av, sym),
        )
    except HTTPException as exc:
        if cached and cached.get("payload") is not None:
            logger.warning(
                "Income annual AV refresh failed for %s; serving stale cache. detail=%s",
                sym,
                getattr(exc, "detail", exc),
            )
            return list(cached["payload"])
        raise

    if rows:
        lf = db.latest_fiscal_date_from_statement_rows(rows)
        await db.upsert_financial_cache(sym, db.DATASET_INCOME_ANNUAL, rows, lf)
    return rows


def get_annual_statement_data(ticker: str) -> List[Dict[str, Any]]:
    return db.sync_wait_awaitable(lambda: fetch_income_annual_cached(ticker))


@router.get("/income-statement/annual/{ticker}")
async def read_annual_income_statement(ticker: str):
    try:
        return await fetch_income_annual_cached(ticker)
    except HTTPException as exc:
        if exc.status_code == 429:
            raise
        logger.exception("Income annual request failed for %s; serving empty list.", ticker)
        return []
    except Exception:
        logger.exception("Income annual unexpected failure for %s; serving empty list.", ticker)
        return []


def build_ttm_quarters_response(
    ticker: str, quarterly_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Payload for /ttmmetrics; pass ``quarterly_data`` to reuse rows from a single income fetch."""
    if quarterly_data is None:
        quarterly_data = get_quarterly_statement_data(ticker)
    income = pd.DataFrame(quarterly_data)
    for col in income.columns:
        if col != "fiscalDateEnding":
            income[col] = pd.to_numeric(income[col], errors='coerce')
    income = income.fillna(0)
    income = income.sort_values(by="fiscalDateEnding", ascending=False)
    result = []
    for i in range(len(income)):
        quarter_data = income.iloc[i].to_dict()
        ttm_metrics = {}
        for col in income.columns:
            if col != "fiscalDateEnding":
                ttm_metrics[f"{col}TTM"] = income[col].iloc[max(0, i):i + 4].sum()
        quarter_data.update(ttm_metrics)
        for key, value in quarter_data.items():
            if isinstance(value, (np.integer, np.floating)):
                quarter_data[key] = value.item()
        result.append(quarter_data)
    return {"ticker": ticker, "quarters": result}


@router.get("/income-statement/quarterly/{ticker}/ttmmetrics")
async def get_ttm_data(ticker: str):
    q = await fetch_income_quarterly_cached(ticker)
    return build_ttm_quarters_response(ticker, q)
