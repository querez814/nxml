from fastapi import APIRouter
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


@router.get("/rsi/{ticker}")
def get_rsi_daily(ticker:str):
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval=daily&time_period=14&series_type=close&apikey={av_api}"
    data = r.get(url).json()
    rsi_daily = data["Technical Analysis: RSI"]
    
    rsi_items = sorted(list(rsi_daily.items()), key=lambda x: x[0], reverse = True)
    rsi_list = []
    
    for date, rsi_data in rsi_items:
        rsi_value = float(rsi_data["RSI"])
        signal = "neutral"
        if rsi_value <= 30:
            signal = "oversold"
        elif rsi_value >= 70:
            signal = "overbought"
            
        rsi_list.append({
            "date": date,
            "rsi": rsi_value,
            "signal": signal
        })

    return rsi_list