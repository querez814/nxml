from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data
from datetime import datetime
from fetch.cashflow import get_quarterly_cashflow_statement_data
from zoneinfo import ZoneInfo
from fetch.balancesheet import get_quarterly_balance_sheet_data
from typing import Optional
import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

TIMEFRAME_FUNCTION_MAP = {
    "intraday": "TIME_SERIES_INTRADAY",
    "daily": "TIME_SERIES_DAILY_ADJUSTED",
    "weekly": "TIME_SERIES_WEEKLY_ADJUSTED",
    "monthly": "TIME_SERIES_MONTHLY_ADJUSTED"
}

@router.get("/prices/{ticker}")
def get_prices(ticker: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()
    time_series = data_json.get("Time Series (Daily)", {})
    transformed_data = []
    for date, values in time_series.items():
        flattened_entry = {"fiscalDateEnding": date}
        for key, value in values.items():
            try:
                flattened_entry[key] = round(float(value), 2)
            except ValueError:
                flattened_entry[key] = 0
        transformed_data.append(flattened_entry)
    prices_df = pd.DataFrame(transformed_data)
    return prices_df.to_dict(orient="records")

@router.get("/close/{ticker}")
def get_closing_prices(ticker: str):
    prices = get_prices(ticker)
    prices_df = pd.DataFrame(prices)
    closing_prices = prices_df["4. close"]
    closing_prices.to_list()
    closing_list = []
    for key in closing_prices:
        closing_list.append(key)
    return closing_list

def candlesticks():
    return

SUPPORTED_INTRADAY_INTERVALS = ["1min", "5min", "15min", "30min", "60min"]

def ensure_est(timestamp_str: str) -> str:
    dt_naive = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    dt_est = dt_naive.replace(tzinfo=ZoneInfo("America/New_York"))
    return dt_est.isoformat()

@router.get("/pricescard")
def get_interval_prices(
    ticker: str,
    timeframe: str = "daily",
    interval: Optional[str] = None,
    outputsize: str = "compact",
    all_intervals: bool = False
):
    timeframe_lower = timeframe.lower()
    alpha_func = TIMEFRAME_FUNCTION_MAP.get(timeframe_lower)
    if not alpha_func:
        raise HTTPException(
            status_code=400,
            detail="Invalid timeframe. Choose from intraday, daily, weekly, or monthly."
        )
    base_url = "https://www.alphavantage.co/query"
    if timeframe_lower != "intraday":
        params = {
            "function": alpha_func,
            "symbol": ticker,
            "apikey": av_api,
            "outputsize": outputsize
        }
        response = r.get(base_url, params=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Alpha Vantage request failed: {response.text}"
            )
        data = response.json()
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail=data["Error Message"])
        if "Note" in data:
            raise HTTPException(status_code=429, detail=data["Note"])
        if timeframe_lower == "daily":
            time_series_key = "Time Series (Daily)"
        elif timeframe_lower == "weekly":
            time_series_key = "Weekly Adjusted Time Series"
        elif timeframe_lower == "monthly":
            time_series_key = "Monthly Adjusted Time Series"
        else:
            raise HTTPException(status_code=400, detail="Unexpected timeframe")
        if time_series_key not in data:
            raise HTTPException(status_code=400, detail="Time series data not found in the response.")
        datapoint_count = len(data[time_series_key])
        return {"datapoint_count": datapoint_count, "data": data[time_series_key]}
    if timeframe_lower == "intraday":
        if all_intervals:
            results = {}
            for intraday_interval in SUPPORTED_INTRADAY_INTERVALS:
                params = {
                    "function": alpha_func,
                    "symbol": ticker,
                    "apikey": str(av_api),
                    "outputsize": outputsize,
                    "interval": intraday_interval
                }
                response = r.get(base_url, params=params)
                if response.status_code != 200:
                    results[intraday_interval] = {"error": f"Request failed: {response.text}"}
                    continue
                data = response.json()
                if "Error Message" in data:
                    results[intraday_interval] = {"error": data["Error Message"]}
                    continue
                if "Note" in data:
                    results[intraday_interval] = {"error": data["Note"]}
                    continue
                time_series_key = f"Time Series ({intraday_interval})"
                if time_series_key not in data:
                    results[intraday_interval] = {"error": "Time series data not found in the response."}
                    continue
                original_series = data[time_series_key]
                converted_series = {}
                for ts, info in original_series.items():
                    converted_series[ensure_est(ts)] = info
                datapoint_count = len(converted_series)
                results[intraday_interval] = {
                    "datapoint_count": datapoint_count,
                    "data": converted_series
                }
            return results
        else:
            chosen_interval = interval if (interval in SUPPORTED_INTRADAY_INTERVALS) else "15min"
            params = {
                "function": alpha_func,
                "symbol": ticker,
                "apikey": av_api,
                "outputsize": outputsize,
                "interval": chosen_interval
            }
            response = r.get(base_url, params=params)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Alpha Vantage request failed: {response.text}"
                )
            data = response.json()
            if "Error Message" in data:
                raise HTTPException(status_code=400, detail=data["Error Message"])
            if "Note" in data:
                raise HTTPException(status_code=429, detail=data["Note"])
            time_series_key = f"Time Series ({chosen_interval})"
            if time_series_key not in data:
                raise HTTPException(status_code=400, detail="Time series data not found in the response.")
            original_series = data[time_series_key]
            converted_series = {}
            for ts, info in original_series.items():
                converted_series[ensure_est(ts)] = info
            datapoint_count = len(converted_series)
            return {
                "interval": chosen_interval,
                "datapoint_count": datapoint_count,
                "data": converted_series
            }
