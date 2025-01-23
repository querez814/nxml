from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

@router.get("/earnings-statement/quarterly/{ticker}")
def get_quarterly_earnings_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")

    data_json = response.json()
    quarterly_reports = data_json.get("quarterlyEarnings", [])
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly earnings data found")

    df = pd.DataFrame(quarterly_reports)
    numeric_cols = ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]
    for col in df.columns:
        if col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)
    df["reportedEPS"] = df["reportedEPS"].apply(lambda x: f"{x:.2f}")
    df["estimatedEPS"] = df["estimatedEPS"].apply(lambda x: f"{x:.2f}")
    df["surprise"] = df["surprise"].apply(lambda x: f"{x:.2f}")
    df["surprisePercentage"] = df["surprisePercentage"].apply(lambda x: f"{x:.1f}%")

    result_df = df.iloc[::-1].reset_index(drop=True)

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]
    for col in numeric_cols:
        series = pd.to_numeric(result_df[col].str.replace("%", ""), errors="coerce") if col == "surprisePercentage" else pd.to_numeric(result_df[col], errors="coerce")
        prev_4 = series.shift(4)
        prev_1 = series.shift(1)
        yoy_series = ((series - prev_4) / prev_4.abs()) * 100
        qoq_series = ((series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        qoq_series = qoq_series.replace([np.inf, -np.inf], 0).fillna(0)

        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        change_df[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")

@router.get("/earnings-statement/annual/{ticker}")
def get_annual_earnings_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")

    data_json = response.json()
    annual_reports = data_json.get("annualEarnings", [])
    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly earnings data found")

    df = pd.DataFrame(annual_reports)
    numeric_cols = ["reportedEPS"]
    for col in df.columns:
        if col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)
    df["reportedEPS"] = df["reportedEPS"].apply(lambda x: f"{x:.2f}")

    result_df = df.iloc[::-1].reset_index(drop=True)

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]
    for col in numeric_cols:
        series = pd.to_numeric(result_df[col], errors="coerce")
        prev_1 = series.shift(1)
        yoy_series = ((series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")
