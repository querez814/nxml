
from fastapi import APIRouter
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any
from datetime import datetime

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

@router.get("/stochastic/{ticker}")
def get_stochastic(ticker: str):
    url = f"https://www.alphavantage.co/query?function=STOCH&symbol={ticker}&interval=daily&fastkperiod=14&slowdperiod=3&apikey={av_api}"
    data = r.get(url).json()
    
    if "Technical Analysis: STOCH" not in data:
        return {"error": "Invalid response from Alpha Vantage. Check API key or request limits."}
    
    stoch_daily = data["Technical Analysis: STOCH"]
    stoch_items = sorted(stoch_daily.items(), key=lambda x: x[0], reverse=True)
    
    stoch_list = []
    prev_slowk = None
    prev_slowd = None

    for date, stoch in stoch_items:
        slowk = float(stoch["SlowK"])
        slowd = float(stoch["SlowD"])
        signal = ""

        # Overbought / Oversold Conditions
        if slowk > 80:
            signal = "Overbought (Potential Sell)"
        elif slowk < 20:
            signal = "Oversold (Potential Buy)"
        
        # Crossover Signals
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
