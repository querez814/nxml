from fastapi import APIRouter, HTTPException
from fetch.av_util import av_get_json_sync
import dotenv as env
import os
import pandas as pd

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()


@router.get("/dividends/{ticker}")
def get_dividends(ticker: str):
    url = f"https://www.alphavantage.co/query?function=DIVIDENDS&symbol={ticker}&apikey={av_api}&datatype=json"
    data_json = av_get_json_sync(url)
    data = data_json.get("data", [])
    return {"symbol": ticker, "dividends": data}


def ttm_dividend_sum(ticker: str) -> float:
    """Sum of cash dividends paid in the trailing 365 days. 0 if none / unknown."""
    payload = get_dividends(ticker)
    rows = payload.get("dividends") or []
    if not rows:
        return 0.0

    df = pd.DataFrame(rows)
    if "ex_dividend_date" not in df.columns or "amount" not in df.columns:
        return 0.0

    df["ex_dividend_date"] = pd.to_datetime(df["ex_dividend_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["ex_dividend_date", "amount"])

    cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=365)
    recent = df[df["ex_dividend_date"] >= cutoff]
    return float(recent["amount"].sum())
