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
import numpy as np
def ensure_numeric(df, exclude_cols=["fiscalDateEnding", "Symbol"]):
    """Converts DataFrame columns to numeric values, excluding specified columns."""
    for col in df.columns:
        if col not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.fillna(0)

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/valuation/quarterly/{ticker}")
def calculate_valuations(ticker:str):
    ttm_data = pd.DataFrame(get_ttm_data(ticker)["quarters"])
    
    print("Available columns:", ttm_data.columns.tolist())
    
    for col in ttm_data.columns:
        if col != "fiscalDateEnding":
            ttm_data[col] = pd.to_numeric(ttm_data[col], errors="coerce")
            
    ttm_data = ttm_data.fillna(0)
    ttm_data = ttm_data.sort_values(by="fiscalDateEnding", ascending=False)
    
    ttm_df = pd.DataFrame()
    ttm_df["fiscalDateEnding"] = ttm_data["fiscalDateEnding"]
    
    column_mapping = {
        "totalRevenueTTM": "totalRevenue_ttm",
        "grossProfitTTM": "grossProfit_ttm",
        "ebitTTM": "ebit_ttm",
        "ebitdaTTM": "ebitda_ttm",
        "operatingIncomeTTM": "operatingIncome_ttm",
        "netIncomeTTM": "netIncome_ttm",
        "reportedEPSTTM": "reportedEPS_ttm"
    }
    
    for old_name, new_name in column_mapping.items():
        if old_name in ttm_data.columns:
            ttm_df[new_name] = ttm_data[old_name]
    
    for col in ttm_df.columns:
        if col != "fiscalDateEnding":
            ttm_df[col] = ttm_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0")
    
    print("TTM DataFrame columns after processing:", ttm_df.columns.tolist())
    print("Sample of processed data:", ttm_df.head())
    
    return ttm_df.to_dict(orient="records")

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

    prices_df["fiscalDateEnding"] = pd.to_datetime(prices_df["fiscalDateEnding"])
    prices_df.sort_values(by="fiscalDateEnding", ascending=False, inplace=True)

    def get_closest_adjusted_close(date):
        matching_row = prices_df[prices_df["fiscalDateEnding"] <= date].head(1)
        if not matching_row.empty:
            return matching_row["5. adjusted close"].values[0]
        return None

    bs["adjustedPrice"] = bs["fiscalDateEnding"].apply(
        lambda date: get_closest_adjusted_close(pd.to_datetime(date))
    )

    if bs["adjustedPrice"].isnull().all():
        raise HTTPException(status_code=404, detail="No adjusted price data available for any balance sheet dates")

    print("Balance Sheet Data with Adjusted Prices:", bs.head())

    for col in ["adjustedPrice", "commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "currentDebt"]:
        bs[col] = pd.to_numeric(bs[col], errors="coerce")

    bs.fillna(0, inplace=True)

    bs["mc"] = bs["commonStockSharesOutstanding"] * bs["adjustedPrice"]
    bs["ev"] = bs["mc"] + bs["cashAndCashEquivalentsAtCarryingValue"] + bs["currentDebt"]

    result = bs.rename(columns={
        "adjustedPrice": "adjustedPrice",
        "commonStockSharesOutstanding": "sharesOutstanding",
        "cashAndCashEquivalentsAtCarryingValue": "cashCashEq",
        "currentDebt": "currentDebt"
    })[["fiscalDateEnding", "adjustedPrice", "sharesOutstanding", "cashCashEq", "currentDebt", "mc", "ev"]]

    if result.empty:
        raise HTTPException(status_code=404, detail="Final result DataFrame is empty")

    return result.to_dict(orient="records")




@router.get("/valuation/quarterly/{ticker}/ttm")
def get_valuation(ticker: str):
    summary = pd.DataFrame([get_summary(ticker)])  
    symbol = summary.loc[0, "Symbol"]  

    cap_struct = pd.DataFrame(get_cap_struct(ticker))
    ttm = pd.DataFrame(calculate_valuations(ticker))

    numeric_cols = [col for col in ttm.columns if col != "fiscalDateEnding"]
    for col in numeric_cols:
        ttm[col] = pd.to_numeric(ttm[col].str.replace(',', ''), errors='coerce')

    cap_struct["Symbol"] = symbol

    cap_struct = ensure_numeric(cap_struct)

    result = pd.DataFrame()
    result["fiscalDateEnding"] = cap_struct["fiscalDateEnding"]
    result["symbol"] = symbol

    print("TTM columns:", ttm.columns.tolist())
    print("Cap struct columns:", cap_struct.columns.tolist())

    result["evtosales"] = (cap_struct["ev"] / ttm["totalRevenue_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtogrossprofit"] = (cap_struct["ev"] / ttm["grossProfit_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtoebit"] = (cap_struct["ev"] / ttm["ebit_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtoebitda"] = (cap_struct["ev"] / ttm["ebitda_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtonetincome"] = (cap_struct["ev"] / ttm["netIncome_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["revenue_per_share_ttm"] = (ttm["totalRevenue_ttm"] / cap_struct["sharesOutstanding"]).replace([np.inf, -np.inf], 0).round(2)
    result["price_to_sales_ratio_ttm"] = (cap_struct["adjustedPrice"] / result["revenue_per_share_ttm"]).replace([np.inf, -np.inf], 0).round(2)

    additional_metrics = [
        "AnalystTargetPrice", "AnalystRatingStrongBuy", "AnalystRatingBuy",
        "AnalystRatingHold", "AnalystRatingSell", "AnalystRatingStrongSell",
        "TrailingPE", "ForwardPE", "Sector", "Industry"
    ]

    for metric in additional_metrics:
        if metric in summary.columns:
            if metric in ["Sector", "Industry"]:
                result[metric] = summary[metric].iloc[0]
            else:
                result[metric] = pd.to_numeric(summary[metric], errors="coerce")

    result = result.fillna(0)
    return result.to_dict(orient="records")
