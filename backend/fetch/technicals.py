from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import requests
import os
import numpy as np
import pandas as pd
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

def fetch_time_series(ticker: str, interval: str) -> Dict:
    """Fetch time series data for support/resistance calculation"""
    url = f"https://www.alphavantage.co/query"
    
    # Map interval to Alpha Vantage function
    function_map = {
        "daily": "TIME_SERIES_DAILY",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY"
    }
    
    function = function_map.get(interval, "TIME_SERIES_DAILY")
    
    params = {
        "function": function,
        "symbol": ticker,
        "outputsize": "full",
        "apikey": AV_API
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Error Message" in data:
        raise HTTPException(status_code=400, detail=data["Error Message"])
    if "Note" in data:
        raise HTTPException(status_code=429, detail=data["Note"])
    
    # Get the appropriate time series key
    time_series_key = list(filter(lambda k: "Time Series" in k, data.keys()))
    if not time_series_key:
        raise HTTPException(status_code=400, detail="No time series data found")
    
    return data[time_series_key[0]]

def calculate_support_resistance(time_series: Dict, periods: int = 20) -> Dict:
    """Calculate support and resistance levels using swing highs/lows and price clusters"""
    # Convert time series to dataframe
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df = df.astype(float)
    
    # Sort by date (newest first)
    df = df.sort_index(ascending=False)
    
    # Limit to requested number of periods
    df = df.head(min(100, len(df)))
    
    # Calculate swing highs and lows
    swing_highs = []
    swing_lows = []
    
    window_size = 5  # Size of window to detect peaks
    
    for i in range(window_size, len(df) - window_size):
        # Check for swing high
        if all(df['high'].iloc[i] > df['high'].iloc[i-j] for j in range(1, window_size+1)) and \
           all(df['high'].iloc[i] > df['high'].iloc[i+j] for j in range(1, window_size+1)):
            swing_highs.append(df['high'].iloc[i])
        
        # Check for swing low
        if all(df['low'].iloc[i] < df['low'].iloc[i-j] for j in range(1, window_size+1)) and \
           all(df['low'].iloc[i] < df['low'].iloc[i+j] for j in range(1, window_size+1)):
            swing_lows.append(df['low'].iloc[i])
    
    # Get the current price
    current_price = df['close'].iloc[0]
    
    # Filter and sort resistance and support levels
    resistance_levels = sorted([price for price in swing_highs if price > current_price])
    support_levels = sorted([price for price in swing_lows if price < current_price], reverse=True)
    
    # Calculate Fibonacci retracement levels
    highest_high = df['high'].max()
    lowest_low = df['low'].min()
    price_range = highest_high - lowest_low
    
    fib_levels = {
        "0.0": round(lowest_low, 2),
        "0.236": round(lowest_low + 0.236 * price_range, 2),
        "0.382": round(lowest_low + 0.382 * price_range, 2),
        "0.5": round(lowest_low + 0.5 * price_range, 2),
        "0.618": round(lowest_low + 0.618 * price_range, 2),
        "0.786": round(lowest_low + 0.786 * price_range, 2),
        "1.0": round(highest_high, 2)
    }
    
    # Get nearest levels
    nearest_resistance = min(resistance_levels, default=None) if resistance_levels else None
    nearest_support = max(support_levels, default=None) if support_levels else None
    
    # If we don't have enough swing points, use Fibonacci levels
    if not nearest_resistance and current_price < highest_high:
        for level in [fib_levels["0.5"], fib_levels["0.618"], fib_levels["0.786"], fib_levels["1.0"]]:
            if level > current_price:
                nearest_resistance = level
                break
    
    if not nearest_support and current_price > lowest_low:
        for level in [fib_levels["0.382"], fib_levels["0.236"], fib_levels["0.0"]]:
            if level < current_price:
                nearest_support = level
                break
    
    return {
        "support_levels": support_levels[:3],  # Top 3 support levels
        "resistance_levels": resistance_levels[:3],  # Top 3 resistance levels
        "nearest_support": nearest_support,
        "nearest_resistance": nearest_resistance,
        "fibonacci_levels": fib_levels
    }

def fetch_moving_averages(ticker: str, interval: str) -> Dict:
    """Fetch SMA and EMA data for different periods"""
    sma_periods = [20, 50, 200]
    ema_periods = [9, 21]
    
    moving_averages = {"sma": {}, "ema": {}}
    
    # Fetch SMAs
    for period in sma_periods:
        sma_data = fetch_indicator(ticker, interval, "SMA", time_period=str(period), series_type="close")
        if sma_data:
            latest_date = max(sma_data.keys())
            moving_averages["sma"][f"SMA{period}"] = float(sma_data[latest_date]["SMA"])
    
    # Fetch EMAs
    for period in ema_periods:
        ema_data = fetch_indicator(ticker, interval, "EMA", time_period=str(period), series_type="close")
        if ema_data:
            latest_date = max(ema_data.keys())
            moving_averages["ema"][f"EMA{period}"] = float(ema_data[latest_date]["EMA"])
    
    return moving_averages

def fetch_volume_indicators(ticker: str, interval: str) -> Dict:
    """Fetch volume-based indicators: OBV and Chaikin Money Flow"""
    volume_indicators = {}
    
    # Fetch OBV (On-Balance Volume)
    try:
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "OBV",
            "symbol": ticker,
            "interval": interval,
            "apikey": AV_API
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if "Technical Analysis: OBV" in data:
            obv_data = data["Technical Analysis: OBV"]
            latest_date = max(obv_data.keys())
            volume_indicators["obv"] = float(obv_data[latest_date]["OBV"])
            
            # Calculate OBV momentum (5-period change)
            dates = sorted(list(obv_data.keys()), reverse=True)[:5]
            if len(dates) >= 5:
                obv_change = (float(obv_data[dates[0]]["OBV"]) - float(obv_data[dates[4]]["OBV"])) / abs(float(obv_data[dates[4]]["OBV"])) * 100
                volume_indicators["obv_momentum"] = round(obv_change, 2)
                volume_indicators["obv_trend"] = "bullish" if obv_change > 0 else "bearish"
    except Exception as e:
        print(f"Error fetching OBV: {e}")
    
    # For now, just return what we have
    return volume_indicators

def analyze_indicators(macd: Dict, rsi: Dict, aroon: Dict, stoch: Dict, 
                      moving_averages: Dict, volume_indicators: Dict, 
                      support_resistance: Dict, date: str, current_price: float) -> Dict[str, Any]:
    """Enhanced indicator analysis including moving averages, volume, and support/resistance"""
    # Original indicators analysis
    macd_val = {
        "value": float(macd[date]["MACD"]),
        "signal_line": float(macd[date]["MACD_Signal"]),
        "histogram": float(macd[date]["MACD_Hist"])
    }
    macd_trend = "bullish" if macd_val["value"] > 0 else "bearish"
    macd_signal = "buy" if macd_val["value"] > macd_val["signal_line"] else "sell"
    
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
    
    # Additional trend signals from moving averages
    ma_trends = []
    
    # Price vs MAs
    sma50 = moving_averages.get("sma", {}).get("SMA50")
    sma200 = moving_averages.get("sma", {}).get("SMA200")
    
    if sma50 and sma200:
        if current_price > sma50 > sma200:
            ma_trends.append("bullish")  # Price above 50-day MA above 200-day MA = bullish
        elif current_price < sma50 < sma200:
            ma_trends.append("bearish")  # Price below 50-day MA below 200-day MA = bearish
        elif sma50 > sma200:
            ma_trends.append("bullish")  # 50-day MA above 200-day MA = bullish trend
        else:
            ma_trends.append("bearish")  # 50-day MA below 200-day MA = bearish trend
    
    # Volume trend
    volume_trend = "neutral"
    if "obv_trend" in volume_indicators:
        volume_trend = volume_indicators["obv_trend"]
    
    # Count all bullish signals
    bullish_count = sum(1 for trend in [macd_trend, rsi_trend, aroon_trend, stoch_trend, *ma_trends, volume_trend] 
                       if "bullish" in trend)
    
    total_signals = 4 + len(ma_trends) + (1 if volume_trend != "neutral" else 0)
    
    # Entry/exit analysis based on support/resistance
    entry_exit = {}
    if support_resistance.get("nearest_support") and support_resistance.get("nearest_resistance"):
        # Calculate risk/reward ratio
        distance_to_support = current_price - support_resistance["nearest_support"]
        distance_to_resistance = support_resistance["nearest_resistance"] - current_price
        
        if distance_to_support > 0 and distance_to_resistance > 0:
            risk_reward = distance_to_resistance / distance_to_support
            
            entry_exit = {
                "potential_entry": current_price if bullish_count / total_signals > 0.6 else None,
                "stop_loss": support_resistance["nearest_support"] * 0.99,  # Just below support
                "take_profit": support_resistance["nearest_resistance"] * 0.98,  # Just below resistance
                "risk_reward_ratio": round(risk_reward, 2)
            }
    
    return {
        "indicators": {
            "macd": {
                "value": macd_val["value"],
                "signal_line": macd_val["signal_line"],
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
            },
            "moving_averages": moving_averages,
            "volume": volume_indicators
        },
        "support_resistance": support_resistance,
        "entry_exit": entry_exit,
        "summary": {
            "trend": "bullish" if bullish_count / total_signals > 0.5 else "bearish",
            "strength": f"{bullish_count}/{total_signals}",
            "confidence": round((max(bullish_count, total_signals - bullish_count) / total_signals) * 100),
            "recommendation": ("buy" if bullish_count / total_signals > 0.6 and rsi_status != "overbought"
                             else "sell" if bullish_count / total_signals < 0.4 and rsi_status != "oversold"
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
        
        # Get current price from latest data
        current_price = float(latest_price["4. close"])
            
        # Fetch basic indicators
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
        
        # Fetch additional indicators
        time_series = fetch_time_series(ticker, interval)
        support_resistance = calculate_support_resistance(time_series)
        moving_averages = fetch_moving_averages(ticker, interval)
        volume_indicators = fetch_volume_indicators(ticker, interval)
        
        # Analyze all indicators
        analysis = analyze_indicators(
            indicators["MACD"],
            indicators["RSI"],
            indicators["AROON"],
            indicators["STOCH"],
            moving_averages,
            volume_indicators,
            support_resistance,
            latest_date,
            current_price
        )
        
        return {
            "ticker": ticker,
            "last_updated": latest_date,
            "price": {
                "current": current_price,
                "open": float(latest_price["1. open"]),
                "high": float(latest_price["2. high"]),
                "low": float(latest_price["3. low"]),
                "volume": int(latest_price["6. volume"])
            },
            **analysis
        }
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))