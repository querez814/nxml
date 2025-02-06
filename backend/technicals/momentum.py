
from fastapi import APIRouter
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any, Tuple
import statistics
from datetime import datetime, timedelta

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

from typing import List, Dict, Any
from fastapi import Path

VALID_INTERVALS = ['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly']

def get_default_limit(interval: str) -> int:
    """Returns appropriate data limit based on the interval"""
    interval_limits = {
        '1min': 100,   
        '5min': 100,    
        '15min': 100,   
        '30min': 100,   
        '60min': 168,   
        'daily': 252,   
        'weekly': 104,  
        'monthly': 60   
    }
    return interval_limits[interval]

def get_time_period(interval: str) -> int:
    """Returns appropriate time period based on the interval"""
    time_periods = {
        '1min': 7,      
        '5min': 9,      
        '15min': 9,     
        '30min': 12,    
        '60min': 14,   
        'daily': 25,    
        'weekly': 14,   
        'monthly': 6    
    }
    return time_periods[interval]

@router.get("/macd/{interval}/{symbol}")
def fetch_macd(
    interval: str = Path(..., enum=VALID_INTERVALS),
    symbol: str = Path(...),
    limit: int = None
) -> List[Dict[str, Any]]:
    default_limit = get_default_limit(interval)
    limit = limit if limit is not None else default_limit
    
    url = f"https://www.alphavantage.co/query?function=MACD&symbol={symbol}&interval={interval}&series_type=close&fastperiod=12&slowperiod=26&signalperiod=9&apikey={av_api}"
    data = r.get(url).json()
    macd = data["Technical Analysis: MACD"]
    items = sorted(list(macd.items()), key=lambda x: x[0], reverse=True)
    return [{"date": date, "macd": float(vals["MACD"]), 
             "macd_signal": float(vals["MACD_Signal"]), 
             "macd_hist": float(vals["MACD_Hist"])} 
            for date, vals in items[:limit]]

@router.get("/ao/{interval}/{symbol}")
def fetch_aroon_oscillator(
    interval: str = Path(..., enum=VALID_INTERVALS),
    symbol: str = Path(...),
    limit: int = None
) -> List[Dict[str, Any]]:
    default_limit = get_default_limit(interval)
    limit = limit if limit is not None else default_limit
    time_period = get_time_period(interval)
    
    url = f"https://www.alphavantage.co/query?function=AROONOSC&symbol={symbol}&interval={interval}&time_period={time_period}&apikey={av_api}"
    data = r.get(url).json()
    ao = data["Technical Analysis: AROONOSC"]
    items = sorted(list(ao.items()), key=lambda x: x[0], reverse=True)
    return [{"date": date, "aroonosc": float(vals["AROONOSC"])} 
            for date, vals in items[:limit]]

@router.get("/mom/{interval}/{symbol}")
def fetch_mom(
    interval: str = Path(..., enum=VALID_INTERVALS),
    symbol: str = Path(...),
    limit: int = None
) -> List[Dict[str, Any]]:
    default_limit = get_default_limit(interval)
    limit = limit if limit is not None else default_limit
    time_period = get_time_period(interval)
    
    url = f"https://www.alphavantage.co/query?function=MOM&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={av_api}"
    data = r.get(url).json()
    mom = data["Technical Analysis: MOM"]
    items = sorted(list(mom.items()), key=lambda x: x[0], reverse=True)
    return [{"date": date, "mom": float(vals["MOM"])} 
            for date, vals in items[:limit]]


@router.get("/stoch/{symbol}")
def fetch_stoch(symbol: str, limit=30) -> List[Dict[str, Any]]:
    url = f"https://www.alphavantage.co/query?function=STOCH&symbol={symbol}&interval=daily&fastkperiod=9&slowkperiod=3&slowdperiod=3&slowkmatype=0&slowdmatype=0&apikey={av_api}"
    data = r.get(url).json()
    stoch = data["Technical Analysis: STOCH"]
    items = sorted(list(stoch.items()), key=lambda x: x[0], reverse=True)
    return [{"date": date, "slowk": float(vals["SlowK"]), 
             "slowd": float(vals["SlowD"])} 
            for date, vals in items[:limit]]

def analyze_trend_pattern(data: List[float]) -> Dict[str, Any]:
    changes = [data[i] - data[i+1] for i in range(len(data)-1)]
    
    direction_changes = sum(1 for i in range(len(changes)-1) if changes[i] * changes[i+1] < 0)
    consistency = 1 - (direction_changes / len(changes))
    
    x = list(range(len(data)))
    slope = statistics.covariance(x, data) / statistics.variance(x)
    
    return {
        "consistency": round(consistency * 100, 2),
        "strength": abs(slope),
        "direction": "up" if slope > 0 else "down"
    }

def calculate_momentum_components(data: List[Dict], field: str) -> Tuple[float, Dict[str, Any]]:
    values = [float(entry[field]) for entry in data]
    
    recent = values[:10]
    historical = values[10:20]
    full_period = values[:30]
    
    trend = analyze_trend_pattern(full_period)
    
    recent_avg = statistics.mean(recent)
    hist_avg = statistics.mean(historical) if historical else recent_avg
    
    volatility = statistics.stdev(full_period) if len(full_period) > 1 else 1
    momentum = ((recent_avg - hist_avg) / volatility) * 50
    
    return max(min(momentum, 100), -100), trend

def calculate_comprehensive_score(macd_data: List[Dict], aroon_data: List[Dict], 
    mom_data: List[Dict], stoch_data: List[Dict]) -> Dict[str, Any]:
    macd_score, macd_trend = calculate_momentum_components(macd_data, "macd")
    aroon_score, aroon_trend = calculate_momentum_components(aroon_data, "aroonosc")
    mom_score, mom_trend = calculate_momentum_components(mom_data, "mom")
    
    stoch_values = [entry["slowk"] for entry in stoch_data]
    stoch_trend = analyze_trend_pattern(stoch_values)
    stoch_score = (stoch_data[0]["slowk"] - 50) * 2
    
    trend_scores = [macd_trend["consistency"], aroon_trend["consistency"], 
                   mom_trend["consistency"]]
    overall_trend_consistency = statistics.mean(trend_scores)
    
    weights = {
        "macd": 0.30,
        "aroon": 0.25,
        "momentum": 0.25,
        "stochastic": 0.10,
        "trend_consistency": 0.10
    }
    
    final_score = (
        weights["macd"] * macd_score +
        weights["aroon"] * aroon_score +
        weights["momentum"] * mom_score +
        weights["stochastic"] * stoch_score +
        weights["trend_consistency"] * overall_trend_consistency
    )
    
    return {
        "score": round(final_score, 2),
        "trend_analysis": {
            "consistency": round(overall_trend_consistency, 2),
            "macd_trend": macd_trend,
            "aroon_trend": aroon_trend,
            "momentum_trend": mom_trend,
            "stochastic_trend": stoch_trend
        },
        "components": {
            "macd": round(macd_score, 2),
            "aroon": round(aroon_score, 2),
            "momentum": round(mom_score, 2),
            "stochastic": round(stoch_score, 2)
        }
    }

def calculate_market_condition(trend_analysis: Dict) -> str:
    consistency = trend_analysis["consistency"]
    component_trends = [
        trend_analysis[f"{component}_trend"]["direction"]
        for component in ["macd", "momentum", "aroon"]
    ]
    
    up_trends = component_trends.count("up")
    down_trends = component_trends.count("down")
    
    if consistency > 75:
        if up_trends > down_trends:
            return "STRONG_UPTREND"
        else:
            return "STRONG_DOWNTREND"
    elif consistency > 50:
        if up_trends > down_trends:
            return "MODERATE_UPTREND"
        else:
            return "MODERATE_DOWNTREND"
    else:
        return "CONSOLIDATION"

@router.get("/momentum/{symbol}")
def get_symbol_momentum(symbol: str):
    try:
        macd_data = fetch_macd(symbol)
        aroon_data = fetch_aroon_oscillator(symbol)
        mom_data = fetch_mom(symbol)
        stoch_data = fetch_stoch(symbol)
        
        analysis = calculate_comprehensive_score(macd_data, aroon_data, mom_data, stoch_data)
        market_condition = calculate_market_condition(analysis["trend_analysis"])
        
        return {
            "symbol": symbol,
            "date": macd_data[0]["date"],
            "momentum_score": analysis["score"],
            "market_condition": market_condition,
            "trend_analysis": analysis["trend_analysis"],
            "component_scores": analysis["components"],
            "period": f"{macd_data[-1]['date']} to {macd_data[0]['date']}"
        }
    except Exception as e:
        return {"error": f"Failed to fetch momentum data: {str(e)}"}

@router.get("/marketmomentum")
def get_market_momentum():
    symbols = ["SPY", "QQQ", "DIA"]
    results = {}
    for sym in symbols:
        results[sym] = get_symbol_momentum(sym)
    return results