from fastapi import APIRouter, HTTPException
from fetch.av_util import av_get_json_sync
import dotenv as env
import os
import pandas as pd

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()


@router.get("/earnings-estimates/{ticker}")
def get_earnings_estimates(ticker: str):
    url = f"https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol={ticker}&apikey={av_api}"
    data_json = av_get_json_sync(url)
    estimates = data_json.get("estimates", [])
    if not estimates:
        return {"symbol": ticker, "estimates": []}

    df = pd.DataFrame(estimates)
    numeric_cols = [
        "eps_estimate_average", "eps_estimate_high", "eps_estimate_low",
        "eps_estimate_analyst_count",
        "revenue_estimate_average", "revenue_estimate_high", "revenue_estimate_low",
        "revenue_estimate_analyst_count",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return {"symbol": ticker, "estimates": df.to_dict(orient="records")}


def forward_eps_and_revenue(ticker: str):
    """Return (fwd_eps_next4q, fwd_revenue_next4q, fwd_eps_growth) or (None, None, None).

    Aggregates the next 4 *fiscal quarter* analyst estimates where `date` is after today.
    Falls back to the nearest fiscal-year estimate if quarterly estimates are missing.
    """
    data = get_earnings_estimates(ticker)
    estimates = data.get("estimates") or []
    if not estimates:
        return None, None, None

    df = pd.DataFrame(estimates)
    if df.empty:
        return None, None, None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    today = pd.Timestamp.today().normalize()
    future_q = df[(df["horizon"] == "fiscal quarter") & (df["date"] >= today)].head(4)

    fwd_eps = None
    fwd_rev = None
    if len(future_q) >= 1:
        fwd_eps = float(future_q["eps_estimate_average"].sum()) if future_q["eps_estimate_average"].notna().any() else None
        fwd_rev = float(future_q["revenue_estimate_average"].sum()) if future_q["revenue_estimate_average"].notna().any() else None
    else:
        future_fy = df[(df["horizon"] == "fiscal year") & (df["date"] >= today)].head(1)
        if not future_fy.empty:
            row = future_fy.iloc[0]
            fwd_eps = float(row["eps_estimate_average"]) if pd.notna(row["eps_estimate_average"]) else None
            fwd_rev = float(row["revenue_estimate_average"]) if pd.notna(row["revenue_estimate_average"]) else None

    fwd_growth = None
    fy = df[df["horizon"] == "fiscal year"].sort_values("date")
    past_fy = fy[fy["date"] < today].tail(1)
    future_fy = fy[fy["date"] >= today].head(1)
    if not past_fy.empty and not future_fy.empty:
        prev_eps = past_fy["eps_estimate_average"].iloc[0]
        next_eps = future_fy["eps_estimate_average"].iloc[0]
        if pd.notna(prev_eps) and pd.notna(next_eps) and prev_eps not in (0, None) and prev_eps != 0:
            try:
                fwd_growth = (float(next_eps) - float(prev_eps)) / abs(float(prev_eps))
            except Exception:
                fwd_growth = None

    return fwd_eps, fwd_rev, fwd_growth
