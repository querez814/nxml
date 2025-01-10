from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np
from fetch.prices import get_prices

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

api_cache = {}

def fetch_indicator_data(url):
    if url in api_cache:
        return api_cache[url]
    response = r.get(url)
    if response.status_code != 200 or "Error" in response.text:
        raise HTTPException(status_code=500, detail=f"API Error: {response.text}")
    data = response.json()
    api_cache[url] = data
    return data



@router.get("/complete/{interval}/{ticker}")
def complete_entry_response(interval:str, ticker:str):
    return 





"""
@router.get("/complete/{interval}/{ticker}")
def complete_response_with_entry_score(interval: str, ticker: str):
    def get_indicator_df(url, technical_key, rename_cols):
        try:
            json_data = fetch_indicator_data(url)
            series = json_data.get(technical_key, {})
            if not series:
                return pd.DataFrame()
            df = (
                pd.DataFrame(series)
                .T
                .reset_index()
                .rename(columns=rename_cols)
            )
            df["fiscalDateEnding"] = df["fiscalDateEnding"].astype(str)
            return df
        except Exception:
            return pd.DataFrame()

    def compute_rolling_zscore(df, col, window=20):
        if df[col].count() < window:
            return df
        roll_mean = df[col].rolling(window=window, min_periods=1).mean()
        roll_std = df[col].rolling(window=window, min_periods=1).std()
        z_col = f"{col}_z"
        df[z_col] = (df[col] - roll_mean) / (roll_std + 1e-9)
        return df

    urls = {
        "SMA_10": f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval={interval}&time_period=10&series_type=close&apikey={av_api}",
        "SMA_50": f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval={interval}&time_period=50&series_type=close&apikey={av_api}",
        "SMA_200": f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval={interval}&time_period=200&series_type=close&apikey={av_api}",
        "RSI": f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval={interval}&time_period=14&series_type=close&apikey={av_api}",
        "ATR": f"https://www.alphavantage.co/query?function=ATR&symbol={ticker}&interval={interval}&time_period=14&apikey={av_api}",
        "OBV": f"https://www.alphavantage.co/query?function=OBV&symbol={ticker}&interval={interval}&apikey={av_api}",
        "EMA": f"https://www.alphavantage.co/query?function=EMA&symbol={ticker}&interval={interval}&time_period=14&series_type=close&apikey={av_api}",
        "AROON": f"https://www.alphavantage.co/query?function=AROON&symbol={ticker}&interval={interval}&time_period=14&apikey={av_api}",
        "ADX": f"https://www.alphavantage.co/query?function=ADX&symbol={ticker}&interval={interval}&time_period=14&apikey={av_api}",
    }

    indicator_dfs = {
        "RSI": get_indicator_df(urls["RSI"], "Technical Analysis: RSI", {"index": "fiscalDateEnding", "RSI": "RSI"}),
        "ATR": get_indicator_df(urls["ATR"], "Technical Analysis: ATR", {"index": "fiscalDateEnding", "ATR": "ATR"}),
        "OBV": get_indicator_df(urls["OBV"], "Technical Analysis: OBV", {"index": "fiscalDateEnding", "OBV": "OBV"}),
        "SMA_10": get_indicator_df(urls["SMA_10"], "Technical Analysis: SMA", {"index": "fiscalDateEnding", "SMA": "SMA"}),
        "SMA_50": get_indicator_df(urls["SMA_50"], "Technical Analysis: SMA", {"index": "fiscalDateEnding", "SMA": "SMA"}),
        "SMA_200": get_indicator_df(urls["SMA_200"], "Technical Analysis: SMA", {"index": "fiscalDateEnding", "SMA": "SMA"}),
        "EMA": get_indicator_df(urls["EMA"], "Technical Analysis: EMA", {"index": "fiscalDateEnding", "EMA": "EMA"}),
        "AROON": get_indicator_df(urls["AROON"], "Technical Analysis: AROON", {"index": "fiscalDateEnding", "Aroon Up": "AROON_Up", "Aroon Down": "AROON_Down"}),
        "ADX": get_indicator_df(urls["ADX"], "Technical Analysis: ADX", {"index": "fiscalDateEnding", "ADX": "ADX"}),
    }

    prices_list = get_prices(ticker)
    prices_df = pd.DataFrame(prices_list)
    prices_df["fiscalDateEnding"] = prices_df["fiscalDateEnding"].astype(str)

    combined_df = prices_df
    for key, df in indicator_dfs.items():
        if df.empty:
            df = pd.DataFrame(columns=["fiscalDateEnding"] + list(df.columns))
        combined_df = pd.merge(combined_df, df, on="fiscalDateEnding", how="left")

    required_columns = [
        "fiscalDateEnding", "1. open", "5. adjusted close", "SMA_10", "SMA_50", "SMA_200",
        "RSI", "ATR", "OBV", "EMA", "AROON_Up", "AROON_Down", "ADX",
    ]
    for col in required_columns:
        if col not in combined_df.columns:
            combined_df[col] = np.nan

    numeric_cols = [col for col in required_columns if col not in ["fiscalDateEnding", "1. open", "5. adjusted close"]]
    for col in numeric_cols:
        combined_df[col] = pd.to_numeric(combined_df[col], errors="coerce")

    for col in numeric_cols:
        compute_rolling_zscore(combined_df, col, window=20)

    def calculate_entry_point_score(row):
        trend_score = (
            (row["SMA_10"] > row["SMA_50"]) * 0.4 +
            (row["SMA_50"] > row["SMA_200"]) * 0.4
        ) * 100

        normalized_rsi = 100 - row["RSI"]
        momentum_score = (normalized_rsi / 100) * 100

        atr_score = 100 - row["ATR_z"] * 10

        volume_score = row["OBV_z"] * 20

        aroon_score = (row["AROON_Up"] - row["AROON_Down"]) * 0.5

        ema_score = row["EMA_z"] * 10

        adx_score = row["ADX"] * 0.5

        entry_score = (
            trend_score * 0.3 +
            momentum_score * 0.2 +
            atr_score * 0.15 +
            volume_score * 0.1 +
            aroon_score * 0.1 +
            ema_score * 0.1 +
            adx_score * 0.05
        )
        return entry_score

    combined_df["Entry_Score"] = combined_df.apply(calculate_entry_point_score, axis=1)
    combined_df["Entry_Score"] = combined_df["Entry_Score"].fillna(0)

    combined_df = combined_df.sort_values(by="fiscalDateEnding", ascending=False)
    combined_df = combined_df.replace([np.inf, -np.inf], np.nan).fillna(0)

    return combined_df.to_dict(orient="records")
"""