from fastapi import APIRouter
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np
from fetch.prices import get_prices



env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()



#RSI ROUTER FOR DEVELOPMENT
@router.get("/rsi/{interval}/{ticker}")
def get_rsi(interval:str, ticker:str):
    #Getting the RSI from the API
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval={interval}&time_period=14&series_type=close&apikey={av_api}"
    response = r.get(url)
    rsi_json = response.json()
    rsi_series = rsi_json.get("Technical Analysis: RSI", {})
    rsi_df_0 = pd.DataFrame(rsi_series)

    return rsi_df_0


@router.get("/macd/{interval}/{ticker}")
def get_macd(interval:str, ticker:str):
    url = f"https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval={interval}&series_type=close&apikey={av_api}"
    response = r.get(url)
    macd_json = response.json() 
    macd_series = macd_json.get("Technical Analysis: MACD")
    macd_df = pd.DataFrame(macd_series)

    return macd_df

from fastapi import APIRouter
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np
from fetch.prices import get_prices

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

@router.get("/complete/{interval}/{ticker}")
def complete_response(interval: str, ticker: str):
    rsi_url = (
        f"https://www.alphavantage.co/query?"
        f"function=RSI&symbol={ticker}&interval={interval}"
        f"&time_period=14&series_type=close&apikey={av_api}"
    )
    rsi_json = r.get(rsi_url).json()
    rsi_series = rsi_json.get("Technical Analysis: RSI", {})
    rsi_df = (
        pd.DataFrame(rsi_series)
        .T
        .reset_index()
        .rename(columns={"index": "fiscalDateEnding", "RSI": "RSI"})
    )
    rsi_df["fiscalDateEnding"] = rsi_df["fiscalDateEnding"].astype(str)

    macd_url = (
        f"https://www.alphavantage.co/query?"
        f"function=MACD&symbol={ticker}&interval={interval}"
        f"&series_type=close&apikey={av_api}"
    )
    macd_json = r.get(macd_url).json()
    macd_series = macd_json.get("Technical Analysis: MACD", {})
    macd_df = (
        pd.DataFrame(macd_series)
        .T
        .reset_index()
        .rename(
            columns={
                "index": "fiscalDateEnding",
                "MACD": "MACD",
                "MACD_Signal": "MACD_Signal",
                "MACD_Hist": "MACD_Hist",
            }
        )
    )
    macd_df["fiscalDateEnding"] = macd_df["fiscalDateEnding"].astype(str)

    bbands_url = (
        f"https://www.alphavantage.co/query?"
        f"function=BBANDS&symbol={ticker}&interval={interval}"
        f"&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey={av_api}"
    )
    bbands_json = r.get(bbands_url).json()
    bbands_series = bbands_json.get("Technical Analysis: BBANDS", {})
    bbands_df = (
        pd.DataFrame(bbands_series)
        .T
        .reset_index()
        .rename(
            columns={
                "index": "fiscalDateEnding",
                "Real Upper Band": "BB_Upper",
                "Real Lower Band": "BB_Lower",
                "Real Middle Band": "BB_Middle",
            }
        )
    )
    bbands_df["fiscalDateEnding"] = bbands_df["fiscalDateEnding"].astype(str)
    adx_url = (
        f"https://www.alphavantage.co/query?"
        f"function=ADX&symbol={ticker}&interval={interval}"
        f"&time_period=10&apikey={av_api}"
    )
    adx_json = r.get(adx_url).json()
    adx_series = adx_json.get("Technical Analysis: ADX", {})
    adx_df = (
        pd.DataFrame(adx_series)
        .T
        .reset_index()
        .rename(columns={"index": "fiscalDateEnding", "ADX": "ADX"})
    )
    adx_df["fiscalDateEnding"] = adx_df["fiscalDateEnding"].astype(str)

    obv_url = (
        f"https://www.alphavantage.co/query?"
        f"function=OBV&symbol={ticker}&interval={interval}&apikey={av_api}"
    )
    obv_json = r.get(obv_url).json()
    obv_series = obv_json.get("Technical Analysis: OBV", {})
    obv_df = (
        pd.DataFrame(obv_series)
        .T
        .reset_index()
        .rename(columns={"index": "fiscalDateEnding", "OBV": "OBV"})
    )
    obv_df["fiscalDateEnding"] = obv_df["fiscalDateEnding"].astype(str)

    ema_url = (
        f"https://www.alphavantage.co/query?"
        f"function=EMA&symbol={ticker}&interval={interval}"
        f"&time_period=10&series_type=open&apikey={av_api}"
    )
    ema_json = r.get(ema_url).json()
    ema_series = ema_json.get("Technical Analysis: EMA", {})
    ema_df = (
        pd.DataFrame(ema_series)
        .T
        .reset_index()
        .rename(columns={"index": "fiscalDateEnding", "EMA": "EMA"})
    )
    ema_df["fiscalDateEnding"] = ema_df["fiscalDateEnding"].astype(str)

    atr_url = (
        f"https://www.alphavantage.co/query?"
        f"function=ATR&symbol={ticker}&interval={interval}"
        f"&time_period=14&apikey={av_api}"
    )
    atr_json = r.get(atr_url).json()
    atr_series = atr_json.get("Technical Analysis: ATR", {})
    atr_df = (
        pd.DataFrame(atr_series)
        .T
        .reset_index()
        .rename(columns={"index": "fiscalDateEnding", "ATR": "ATR"})
    )
    atr_df["fiscalDateEnding"] = atr_df["fiscalDateEnding"].astype(str)

    prices_list = get_prices(ticker)  
    prices_df = pd.DataFrame(prices_list)
    prices_df["fiscalDateEnding"] = prices_df["fiscalDateEnding"].astype(str)

    combined_df = pd.merge(prices_df, rsi_df, on="fiscalDateEnding", how="inner")
    combined_df = pd.merge(combined_df, macd_df, on="fiscalDateEnding", how="inner")
    combined_df = pd.merge(combined_df, bbands_df, on="fiscalDateEnding", how="inner")
    combined_df = pd.merge(combined_df, adx_df, on="fiscalDateEnding", how="inner")
    combined_df = pd.merge(combined_df, obv_df, on="fiscalDateEnding", how="inner")
    combined_df = pd.merge(combined_df, ema_df, on="fiscalDateEnding", how="inner")
    combined_df = pd.merge(combined_df, atr_df, on="fiscalDateEnding", how="inner")
    columns_we_want = [
        "fiscalDateEnding",
        "1. open",
        "5. adjusted close",
        "RSI",
        "MACD",
        "MACD_Signal",
        "MACD_Hist",
        "BB_Upper",
        "BB_Lower",
        "BB_Middle",
        "ADX",
        "OBV",
        "EMA",
        "ATR",
    ]
    combined_df = combined_df[columns_we_want]

    numeric_cols = ["RSI", "MACD", "MACD_Signal", "MACD_Hist", 
                    "ADX", "OBV", "EMA", "ATR"]
    for col in numeric_cols:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

    combined_df = combined_df.sort_values(by="fiscalDateEnding", ascending=True)

    def compute_rolling_zscore(df, col, window=20):
        roll_mean = df[col].rolling(window=window).mean()
        roll_std = df[col].rolling(window=window).std()
        z_col = f"{col}_z"
        df[z_col] = (df[col] - roll_mean) / (roll_std + 1e-9) 
        return df

    indicators_for_z = ["RSI", "MACD", "MACD_Hist", "ADX", "OBV", "EMA", "ATR"]
    for ind in indicators_for_z:
        compute_rolling_zscore(combined_df, ind, window=20)


    z_cols = [f"{ind}_z" for ind in indicators_for_z]
    combined_df["Z_Composite"] = combined_df[z_cols].sum(axis=1)

    combined_df = combined_df.sort_values(by="fiscalDateEnding", ascending=False)
    combined_df = combined_df.replace([np.inf, -np.inf], np.nan)

    combined_df = combined_df.fillna(0)


    #  RETURN EVERYTHING AS JSON 
    return combined_df.to_dict(orient="records")
