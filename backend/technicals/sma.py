from fastapi import APIRouter, HTTPException
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any
from fetch.prices import get_closing_prices
import statistics
from datetime import datetime, timedelta

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

SMA_TIME_PERIODS_MAP = {
    "1min": {"sma20": 5,  "sma50": 10, "sma200": 30},
    "5min": {"sma20": 10, "sma50": 20, "sma200": 60},
    "15min": {"sma20": 14, "sma50": 28, "sma200": 100},
    "30min": {"sma20": 20, "sma50": 50, "sma200": 200},
    "60min": {"sma20": 20, "sma50": 50, "sma200": 200},
    "daily": {"sma20": 20, "sma50": 50, "sma200": 200},
    "weekly": {"sma20": 10, "sma50": 25, "sma200": 100},
    "monthly": {"sma20": 5, "sma50": 15, "sma200": 50}
}

@router.get("/smas/{interval}/{ticker}")
def get_smas(interval: str, ticker: str):
    if interval not in SMA_TIME_PERIODS_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid interval '{interval}'. Supported intervals are: {', '.join(SMA_TIME_PERIODS_MAP.keys())}"
        )
    time_periods = SMA_TIME_PERIODS_MAP[interval]

    url_20 = (
        f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}"
        f"&interval={interval}&time_period={time_periods['sma20']}"
        f"&series_type=close&apikey={av_api}"
    )
    url_50 = (
        f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}"
        f"&interval={interval}&time_period={time_periods['sma50']}"
        f"&series_type=close&apikey={av_api}"
    )
    url_200 = (
        f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}"
        f"&interval={interval}&time_period={time_periods['sma200']}"
        f"&series_type=close&apikey={av_api}"
    )

    data_20 = r.get(url_20).json()
    data_50 = r.get(url_50).json()
    data_200 = r.get(url_200).json()

    if ("Technical Analysis: SMA" not in data_20 or
        "Technical Analysis: SMA" not in data_50 or
        "Technical Analysis: SMA" not in data_200):
        raise HTTPException(status_code=500, detail="Error retrieving SMA data from Alpha Vantage.")

    sma_20 = data_20["Technical Analysis: SMA"]
    sma_50 = data_50["Technical Analysis: SMA"]
    sma_200 = data_200["Technical Analysis: SMA"]

    sma_20_items = sorted(list(sma_20.items()), key=lambda x: x[0], reverse=True)
    sma_50_items = sorted(list(sma_50.items()), key=lambda x: x[0], reverse=True)
    sma_200_items = sorted(list(sma_200.items()), key=lambda x: x[0], reverse=True)

    closing_prices_list = get_closing_prices(ticker)
    sma_points = []
    price_index = 0
    prev_close = None
    prev_sma20 = None
    prev_sma50 = None
    prev_sma200 = None

    i, j, k = 0, 0, 0
    while i < len(sma_20_items) and j < len(sma_50_items) and k < len(sma_200_items):
        date_20, vals_20 = sma_20_items[i]
        date_50, vals_50 = sma_50_items[j]
        date_200, vals_200 = sma_200_items[k]
        max_date = max(date_20, date_50, date_200)

        current_close = closing_prices_list[price_index] if price_index < len(closing_prices_list) else None
        current_sma20 = float(vals_20["SMA"]) if date_20 == max_date else None
        current_sma50 = float(vals_50["SMA"]) if date_50 == max_date else None
        current_sma200 = float(vals_200["SMA"]) if date_200 == max_date else None

        point = {
            "date": max_date,
            "Close": current_close,
            "sma20": current_sma20,
            "sma50": current_sma50,
            "sma200": current_sma200
        }

        if prev_close is not None and prev_sma20 is not None and current_close is not None and current_sma20 is not None:
            if current_close > current_sma20 and prev_close < prev_sma20:
                point["price_cross_sma20"] = "bullish"
            elif current_close < current_sma20 and prev_close > prev_sma20:
                point["price_cross_sma20"] = "bearish"

        if prev_close is not None and prev_sma50 is not None and current_close is not None and current_sma50 is not None:
            if current_close > current_sma50 and prev_close < prev_sma50:
                point["price_cross_sma50"] = "bullish"
            elif current_close < current_sma50 and prev_close > prev_sma50:
                point["price_cross_sma50"] = "bearish"

        if prev_close is not None and prev_sma200 is not None and current_close is not None and current_sma200 is not None:
            if current_close > current_sma200 and prev_close < prev_sma200:
                point["price_cross_sma200"] = "bullish"
            elif current_close < current_sma200 and prev_close > prev_sma200:
                point["price_cross_sma200"] = "bearish"

        if prev_sma20 is not None and prev_sma50 is not None and current_sma20 is not None and current_sma50 is not None:
            if current_sma20 > current_sma50 and prev_sma20 < prev_sma50:
                point["sma20_cross_sma50"] = "bullish"
            elif current_sma20 < current_sma50 and prev_sma20 > prev_sma50:
                point["sma20_cross_sma50"] = "bearish"

        if prev_sma20 is not None and prev_sma200 is not None and current_sma20 is not None and current_sma200 is not None:
            if current_sma20 > current_sma200 and prev_sma20 < prev_sma200:
                point["sma20_cross_sma200"] = "bullish"
            elif current_sma20 < current_sma200 and prev_sma20 > prev_sma200:
                point["sma20_cross_sma200"] = "bearish"

        if prev_sma50 is not None and prev_sma200 is not None and current_sma50 is not None and current_sma200 is not None:
            if current_sma50 > current_sma200 and prev_sma50 < prev_sma200:
                point["sma50_cross_sma200"] = "bullish"
            elif current_sma50 < current_sma200 and prev_sma50 > prev_sma200:
                point["sma50_cross_sma200"] = "bearish"

        sma_points.append(point)

        prev_close = current_close
        prev_sma20 = current_sma20
        prev_sma50 = current_sma50
        prev_sma200 = current_sma200

        if date_20 == max_date:
            i += 1
        if date_50 == max_date:
            j += 1
        if date_200 == max_date:
            k += 1
        price_index += 1

    while i < len(sma_20_items):
        date_20, vals_20 = sma_20_items[i]
        current_close = closing_prices_list[price_index] if price_index < len(closing_prices_list) else None
        sma_points.append({
            "date": date_20,
            "Close": current_close,
            "sma20": float(vals_20["SMA"]),
            "sma50": None,
            "sma200": None
        })
        i += 1
        price_index += 1

    while j < len(sma_50_items):
        date_50, vals_50 = sma_50_items[j]
        current_close = closing_prices_list[price_index] if price_index < len(closing_prices_list) else None
        sma_points.append({
            "date": date_50,
            "Close": current_close,
            "sma20": None,
            "sma50": float(vals_50["SMA"]),
            "sma200": None
        })
        j += 1
        price_index += 1

    while k < len(sma_200_items):
        date_200, vals_200 = sma_200_items[k]
        current_close = closing_prices_list[price_index] if price_index < len(closing_prices_list) else None
        sma_points.append({
            "date": date_200,
            "Close": current_close,
            "sma20": None,
            "sma50": None,
            "sma200": float(vals_200["SMA"])
        })
        k += 1
        price_index += 1

    return sma_points