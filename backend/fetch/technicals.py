from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import requests
import os
from datetime import datetime
from fetch.prices import get_prices


router = APIRouter()
AV_API = os.getenv("ALPHA_VANTAGE")

def fetch_indicator(ticker: str, interval: str, indicator: str, **params) -> Dict:
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": indicator,
        "symbol": ticker,
        "interval": interval,
        "apikey": AV_API,
        **params
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Error Message" in data:
        raise HTTPException(status_code=400, detail=data["Error Message"])
    if "Note" in data:
        raise HTTPException(status_code=429, detail=data["Note"])
        
    return data.get(f"Technical Analysis: {indicator}", {})

def analyze_indicators(macd: Dict, rsi: Dict, aroon: Dict, stoch: Dict, date: str) -> Dict[str, Any]:
    macd_val = {
        "value": float(macd[date]["MACD"]),
        "signal": float(macd[date]["MACD_Signal"]),
        "histogram": float(macd[date]["MACD_Hist"])
    }
    macd_trend = "bullish" if macd_val["value"] > 0 else "bearish"
    macd_signal = "buy" if macd_val["value"] > macd_val["signal"] else "sell"
    
    rsi_val = float(rsi[date]["RSI"])
    rsi_status = "overbought" if rsi_val > 70 else "oversold" if rsi_val < 30 else "neutral"
    rsi_trend = "bullish" if rsi_val > 50 else "bearish"
    
    aroon_up = float(aroon[date]["Aroon Up"])
    aroon_down = float(aroon[date]["Aroon Down"])
    aroon_trend = ("strong_bullish" if aroon_up > 70 and aroon_down < 30 else
                  "strong_bearish" if aroon_down > 70 and aroon_up < 30 else
                  "bullish" if aroon_up > aroon_down else "bearish")
    
    k_line = float(stoch[date]["SlowK"])
    d_line = float(stoch[date]["SlowD"])
    stoch_status = "overbought" if k_line > 80 else "oversold" if k_line < 20 else "neutral"
    stoch_trend = "bullish" if k_line > d_line else "bearish"
    
    bullish_count = sum(1 for trend in [macd_trend, rsi_trend, aroon_trend, stoch_trend] 
                       if "bullish" in trend)
    
    return {
        "indicators": {
            "macd": {
                "value": macd_val["value"],
                "signal_line": macd_val["signal"],
                "histogram": macd_val["histogram"],
                "trend": macd_trend,
                "signal": macd_signal
            },
            "rsi": {
                "value": rsi_val,
                "status": rsi_status,
                "trend": rsi_trend
            },
            "aroon": {
                "up": aroon_up,
                "down": aroon_down,
                "trend": aroon_trend
            },
            "stochastic": {
                "k_line": k_line,
                "d_line": d_line,
                "status": stoch_status,
                "trend": stoch_trend
            }
        },
        "summary": {
            "trend": "bullish" if bullish_count >= 3 else "bearish",
            "recommendation": ("buy" if bullish_count >= 3 and rsi_status != "overbought"
                             else "sell" if bullish_count <= 1 and rsi_status != "oversold"
                             else "hold")
        }
    }

@router.get("/technical-analysis/{interval}/{ticker}")
async def technical_analysis(interval: str, ticker: str):
    try:
        prices = get_prices(ticker)
        latest_price = prices[0] if prices else None
        
        if not latest_price:
            raise HTTPException(status_code=404, detail="No price data available")
            
        indicators = {
            "MACD": fetch_indicator(ticker, interval, "MACD", series_type="close"),
            "RSI": fetch_indicator(ticker, interval, "RSI", time_period="14", series_type="close"),
            "AROON": fetch_indicator(ticker, interval, "AROON", time_period="14"),
            "STOCH": fetch_indicator(ticker, interval, "STOCH")
        }
        
        dates = set.intersection(*[set(ind.keys()) for ind in indicators.values()])
        if not dates:
            raise HTTPException(status_code=404, detail="No overlapping data found")
            
        latest_date = max(dates)
        
        analysis = analyze_indicators(
            indicators["MACD"],
            indicators["RSI"],
            indicators["AROON"],
            indicators["STOCH"],
            latest_date
        )
        
        return {
            "ticker": ticker,
            "last_updated": latest_date,
            "price": {
                "current": float(latest_price["4. close"]),
                "open": float(latest_price["1. open"]),
                "high": float(latest_price["2. high"]),
                "low": float(latest_price["3. low"]),
                "volume": int(latest_price["6. volume"])
            },
            **analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))