from fastapi import APIRouter, HTTPException
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any
from datetime import datetime

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

STOCH_PARAMS_MAP = {
    "1min": {"fastkperiod": 5,  "slowdperiod": 3},
    "5min": {"fastkperiod": 10, "slowdperiod": 3},
    "15min": {"fastkperiod": 14, "slowdperiod": 3},
    "30min": {"fastkperiod": 14, "slowdperiod": 3},
    "60min": {"fastkperiod": 14, "slowdperiod": 3},
    "daily": {"fastkperiod": 14, "slowdperiod": 3},
    "weekly": {"fastkperiod": 14, "slowdperiod": 3},
    "monthly": {"fastkperiod": 14, "slowdperiod": 3}
}

@router.get("/stochastic/{interval}/{ticker}")
def get_stochastic(interval: str, ticker: str):
    if interval not in STOCH_PARAMS_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid interval '{interval}'. Supported intervals are: {', '.join(STOCH_PARAMS_MAP.keys())}"
        )
    params = STOCH_PARAMS_MAP[interval]
    url = (
        f"https://www.alphavantage.co/query?function=STOCH"
        f"&symbol={ticker}"
        f"&interval={interval}"
        f"&fastkperiod={params['fastkperiod']}"
        f"&slowdperiod={params['slowdperiod']}"
        f"&apikey={av_api}"
    )
    data = r.get(url).json()

    if "Technical Analysis: STOCH" not in data:
        return {"error": "Invalid response from Alpha Vantage. Check API key or request limits."}

    stoch_daily = data["Technical Analysis: STOCH"]
    stoch_items = sorted(stoch_daily.items(), key=lambda x: x[0], reverse=True)

    stoch_list = []
    prev_slowk = None
    prev_slowd = None

    for date, stoch in stoch_items:
        try:
            slowk = float(stoch["SlowK"])
            slowd = float(stoch["SlowD"])
        except (KeyError, ValueError):
            continue

        signal = ""

        if slowk > 80:
            signal = "Overbought (Potential Sell)"
        elif slowk < 20:
            signal = "Oversold (Potential Buy)"

        if prev_slowk is not None and prev_slowd is not None:
            if prev_slowk < prev_slowd and slowk > slowd:
                signal = "Bullish Crossover (Buy Signal)"
            elif prev_slowk > prev_slowd and slowk < slowd:
                signal = "Bearish Crossover (Sell Signal)"

        stoch_list.append({
            "date": date,
            "slowk": slowk,
            "slowd": slowd,
            "signal": signal
        })

        prev_slowk = slowk
        prev_slowd = slowd

    return stoch_list
