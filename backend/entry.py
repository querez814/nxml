
from fastapi import APIRouter
import dotenv as env
import os
import requests as r

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

def fetch_sma(symbol, time_period):
    url = f"https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=daily&time_period={time_period}&series_type=close&apikey={av_api}"
    data = r.get(url).json()
    val = list(data["Technical Analysis: SMA"].values())[0]["SMA"]
    return float(val)

def fetch_adx(symbol):
    url = f"https://www.alphavantage.co/query?function=ADX&symbol={symbol}&interval=daily&time_period=14&apikey={av_api}"
    data = r.get(url).json()
    val = list(data["Technical Analysis: ADX"].values())[0]["ADX"]
    return float(val)

def fetch_bbands(symbol):
    url = f"https://www.alphavantage.co/query?function=BBANDS&symbol={symbol}&interval=daily&time_period=20&series_type=close&nbdevup=2&nbdevdn=2&apikey={av_api}"
    data = r.get(url).json()
    latest = list(data["Technical Analysis: BBANDS"].values())[0]
    upper = float(latest["Real Upper Band"])
    lower = float(latest["Real Lower Band"])
    return upper, lower

def analyze_sma_crossover(sma_50, sma_200):
    if sma_50 > sma_200:
        return "bullish"
    elif sma_50 < sma_200:
        return "bearish"
    return "neutral"

def analyze_adx(adx_val):
    if adx_val >= 25:
        return "strong"
    elif adx_val >= 20:
        return "moderate"
    return "weak"

def analyze_bbands(upper, lower):
    width = upper - lower
    if width > 10:
        return "high"
    elif width < 3:
        return "low"
    return "medium"

def get_env_for_symbol(symbol):
    sma50 = fetch_sma(symbol, 50)
    sma200 = fetch_sma(symbol, 200)
    adx_val = fetch_adx(symbol)
    upper, lower = fetch_bbands(symbol)
    crossover = analyze_sma_crossover(sma50, sma200)
    adx_strength = analyze_adx(adx_val)
    bb_volatility = analyze_bbands(upper, lower)

    return {
        "symbol": symbol,
        "trend_overview": {
            "short_vs_long_sma": crossover,
            "simple_explanation": (
                f"Short-term trend (50-day average) is {crossover.upper()} "
                f"compared to the long-term trend (200-day average)."
            )
        },
        "trend_strength": {
            "adx_value": round(adx_val, 2),
            "rating": adx_strength,
            "meaning": (
                "The current price trend is strong."
                if adx_strength == "strong"
                else "The trend is moderate."
                if adx_strength == "moderate"
                else "The market doesn't show a strong trend right now."
            )
        },
        "volatility": {
            "bb_width_rating": bb_volatility,
            "meaning": (
                "Price fluctuations have been large, so expect bigger moves."
                if bb_volatility == "high"
                else "Price fluctuations have been relatively small."
                if bb_volatility == "low"
                else "Price movements are moderate, not too large or too small."
            )
        }
    }

@router.get("/marketenv")
def get_market_env():
    symbols = ["SPY", "QQQ", "DIA"]
    results = {}
    for sym in symbols:
        results[sym] = get_env_for_symbol(sym)
    return results


