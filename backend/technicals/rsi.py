from fastapi import APIRouter, HTTPException
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any, Tuple
import statistics
from datetime import datetime, timedelta
from fetch.prices import get_closing_prices
import json

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

TIME_PERIOD_MAP = {
    "1min": 5,
    "5min": 14,
    "15min": 14,
    "30min": 14,
    "60min": 14,
    "daily": 14,
    "weekly": 10,
    "monthly": 7
}

@router.get("/rsi/{interval}/{ticker}")
def get_rsi(ticker: str, interval: str):
    # Check if the provided interval is supported.
    if interval not in TIME_PERIOD_MAP:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid interval '{interval}'. "
                "Supported intervals are: " + ", ".join(TIME_PERIOD_MAP.keys())
            )
        )

    time_period = TIME_PERIOD_MAP[interval]

    url = (
        f"https://www.alphavantage.co/query?function=RSI"
        f"&symbol={ticker}"
        f"&interval={interval}"
        f"&time_period={time_period}"
        f"&series_type=close"
        f"&apikey={av_api}"
    )

    response = r.get(url)
    data = response.json()

    technical_analysis_key = "Technical Analysis: RSI"
    if technical_analysis_key not in data:
        raise HTTPException(
            status_code=500,
            detail="Error retrieving RSI data from Alpha Vantage."
        )

    rsi_data = data[technical_analysis_key]
    sorted_items = sorted(rsi_data.items(), key=lambda x: x[0], reverse=True)
    rsi_list = []

    for date, values in sorted_items:
        try:
            rsi_value = float(values["RSI"])
        except (ValueError, KeyError):
            continue  

        if rsi_value <= 30:
            signal = "oversold"
        elif rsi_value >= 70:
            signal = "overbought"
        else:
            signal = "neutral"

        rsi_list.append({
            "date": date,
            "rsi": rsi_value,
            "signal": signal
        })

    return rsi_list