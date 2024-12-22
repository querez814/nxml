from fastapi import APIRouter, HTTPException
from fetch.prices import get_prices
import requests as r
import dotenv as env
import os
import pandas as pd
from fetch.earnings import get_quarterly_earnings_data 
from fetch.income_statement import get_ttm_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
from fetch.summary import get_summary


env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/valuation/quarterly/{ticker}")
def calculate_valuations(ticker:str):
    ttm_data = pd.DataFrame(get_ttm_data(ticker)["quarters"])
    for col in ttm_data.columns:
        if col!="fiscalDateEnding":
            ttm_data[col]=pd.to_numeric(ttm_data[col],errors="coerce")
            
    ttm_data = ttm_data.fillna(0)
    
    ttm_data = ttm_data.sort_values(by="fiscalDateEnding",ascending=False)
    ttm_df = pd.DataFrame()
    ttm_df["totalRevenue_ttm"] = ttm_data["totalRevenue_ttm"]
    ttm_df["grossProfit_ttm"] = ttm_data["grossProfit_ttm"]
    ttm_df["ebit_ttm"] = ttm_data["ebit_ttm"]
    ttm_df["ebitda_ttm"] = ttm_data["ebitda_ttm"]
    ttm_df["operatingIncome_ttm"] = ttm_data["operatingIncome_ttm"]
    ttm_df["netIncome_ttm"] = ttm_data["netIncome_ttm"]
    ttm_df["reportedEPS_ttm"] = ttm_data["reportedEPS_ttm"]

    for col in ttm_df.columns:
        if col != "fiscalDateEnding":
            ttm_df[col] = ttm_df[col].apply(lambda x:f"{x:.2f}" if pd.notnull(x) else"0")
    
    ttm_df = ttm_df.to_dict(orient="records")

    return ttm_df

@router.get("/capitalstructure/quarterly/{ticker}")
def get_cap_struct(ticker: str):
    bs = pd.DataFrame(get_quarterly_balance_sheet_data(ticker))
    if bs.empty:
        raise HTTPException(status_code=404, detail="No data returned from get_quarterly_balance_sheet_data")

    print("Balance Sheet Data:", bs.head())

    prices = get_prices(ticker)
    if not prices:
        raise HTTPException(status_code=404, detail="No data returned from get_prices")

    print("Prices Data:", prices[:5])  

    if isinstance(prices, list):
        prices_df = pd.DataFrame(prices)
    else:
        raise ValueError("Prices data is not in the expected format (list of dictionaries).")

    if prices_df.empty:
        raise HTTPException(status_code=404, detail="Prices DataFrame is empty")

    print("Prices DataFrame:", prices_df.head())

    if "fiscalDateEnding" not in prices_df.columns or "5. adjusted close" not in prices_df.columns:
        raise KeyError("Expected columns 'fiscalDateEnding' or '5. adjusted close' are missing in prices data.")

    fiscal_dates = bs["fiscalDateEnding"].tolist()
    print("Fiscal Dates from Balance Sheet:", fiscal_dates)

    filtered_prices = prices_df[prices_df["fiscalDateEnding"].isin(fiscal_dates)][["fiscalDateEnding", "5. adjusted close"]]
    if filtered_prices.empty:
        raise HTTPException(status_code=404, detail="No matching fiscal dates found in prices data")

    print("Filtered Prices:", filtered_prices.head())

    merged = pd.merge(filtered_prices, bs, on="fiscalDateEnding", how="left")
    if merged.empty:
        raise HTTPException(status_code=404, detail="Merged DataFrame is empty")

    print("Merged DataFrame:", merged.head())

    for col in ["5. adjusted close", "commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "currentDebt"]:
        merged[col] = pd.to_numeric(merged[col], errors="coerce")

    merged.fillna(0, inplace=True)

    merged["mc"] = merged["commonStockSharesOutstanding"] * merged["5. adjusted close"]
    merged["ev"] = merged["mc"] + merged["cashAndCashEquivalentsAtCarryingValue"] + merged["currentDebt"]

    result = merged.rename(columns={
        "5. adjusted close": "adjustedPrice",
        "commonStockSharesOutstanding": "shares_outstanding",
        "cashAndCashEquivalentsAtCarryingValue": "cash_cash_eq",
        "currentDebt": "currentDebt"
    })[["fiscalDateEnding", "adjustedPrice", "shares_outstanding", "cash_cash_eq", "currentDebt", "mc", "ev"]]

    if result.empty:
        raise HTTPException(status_code=404, detail="Final result DataFrame is empty")

    return result.to_dict(orient="records")


@router.get("/valuation/quarterly/{ticker}/ttm")
def get_valuation(ticker: str):
    summary = pd.DataFrame([get_summary(ticker)])  
    symbol = summary.loc[0, "Symbol"]  

    cap_struct = pd.DataFrame(get_cap_struct(ticker))
    ttm = pd.DataFrame(calculate_valuations(ticker))
    earnings = pd.DataFrame(get_quarterly_earnings_data(ticker))

    cap_struct["Symbol"] = symbol

    additional_metrics = [
        "AnalystTargetPrice",
        "AnalystRatingStrongBuy",
        "AnalystRatingBuy",
        "AnalystRatingHold",
        "AnalystRatingSell",
        "AnalystRatingStrongSell",
        "TrailingPE",
        "ForwardPE",
        "Sector", "Industry"
    ]
    exclude_cols=["fiscalDateEnding", "Symbol","Sector","Industry"]
    def ensure_numeric(df, exclude_cols=["fiscalDateEnding", "Symbol","Sector","Industry"]):
        for col in df.columns:
            if col not in exclude_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    metrics = {}
    for metric in additional_metrics:
        if metric not in exclude_cols:
            metrics[metric] = pd.to_numeric(summary.loc[0, metric], errors="coerce")

    cap_struct = ensure_numeric(cap_struct)
    ttm = ensure_numeric(ttm)
    earnings = ensure_numeric(earnings)

    result = pd.DataFrame()

    if "ev" in cap_struct.columns and "totalRevenue_ttm" in ttm.columns:
        result["fiscalDateEnding"] = cap_struct["fiscalDateEnding"]
        result["symbol"] = cap_struct["Symbol"]
        result["evtosales"] = (cap_struct["ev"] / ttm["totalRevenue_ttm"]).round(2)
        result["evtogrossprofit"] = (cap_struct["ev"] / ttm["grossProfit_ttm"]).round(2)
        result["evtoebit"] = (cap_struct["ev"] / ttm["ebit_ttm"]).round(2)
        result["evtoebitda"] = (cap_struct["ev"] / ttm["ebitda_ttm"]).round(2)
        result["evtonetincome"] = (cap_struct["ev"] / ttm["netIncome_ttm"]).round(2)
        result["revenue_per_share_ttm"] = (ttm["totalRevenue_ttm"] / cap_struct["shares_outstanding"]).round(2)
        result["price_to_sales_ratio_ttm"] = (cap_struct["adjustedPrice"] / result["revenue_per_share_ttm"]).round(2)
    else:
        raise KeyError("Required columns 'ev' or 'totalRevenue_ttm' are missing in the input data.")

    for metric, value in metrics.items():
        result[metric] = value

    result.fillna(0, inplace=True)
    result.replace([float('inf'), -float('inf')], 0, inplace=True)

    return result.to_dict(orient="records")

