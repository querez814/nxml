from fastapi import APIRouter, HTTPException, Query
import os
import dotenv as env
import requests as r
from datetime import datetime, timedelta

env.load_dotenv()  
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

@router.get("/macdr/{interval}/{ticker}")
def macd_dynamic(
    interval: str,
    ticker: str,
    days: int = Query(365, description="Number of days to look back for MACD data")
):
    url = (
        f"https://www.alphavantage.co/query?function=MACD"
        f"&symbol={ticker}"
        f"&interval={interval}"
        f"&series_type=close"
        f"&apikey={av_api}"
    )
    
    response = r.get(url)
    data = response.json()
    
    if "Technical Analysis: MACD" not in data:
        raise HTTPException(
            status_code=500,
            detail="Error retrieving MACD data from Alpha Vantage."
        )
    
    macd_data = data["Technical Analysis: MACD"]
    
    cutoff_date = datetime.now() - timedelta(days=days)
    result = []
    
    for date_str, values in macd_data.items():
        dt = None
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        if dt is None:
            continue  
        
        if dt >= cutoff_date:
            try:
                macd_value  = float(values["MACD"])
                macd_signal = float(values["MACD_Signal"])
                macd_hist   = float(values["MACD_Hist"])
            except (KeyError, ValueError):
                continue
            result.append({
                "date": date_str,
                "macd": macd_value,
                "macd_signal": macd_signal,
                "macd_hist": macd_hist
            })
    
    result.sort(key=lambda x: x["date"], reverse=True)
    
    return result
