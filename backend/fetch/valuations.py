
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

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

def ensure_numeric(df, exclude_cols=["fiscalDateEnding", "Symbol"]):
    for col in df.columns:
        if col not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.fillna(0)

@router.get("/valuation/quarterly/{ticker}")
def calculate_valuations(ticker: str):
    ttm_data = pd.DataFrame(get_ttm_data(ticker)["quarters"])
    
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
    
    return ttm_df.to_dict(orient="records")

def get_cap_struct(ticker: str):
    ticker = get_summary(ticker)["Symbol"]
    try:
        bs_data = get_quarterly_balance_sheet_data(ticker)
        bs = pd.DataFrame(bs_data)
        if bs.empty:
            raise HTTPException(status_code=404, detail="No balance sheet data available")
            
        prices = get_prices(ticker)
        if not prices:
            raise HTTPException(status_code=404, detail="No price data available")
            
        prices_df = pd.DataFrame(prices)
        
        prices_df["fiscalDateEnding"] = pd.to_datetime(prices_df["fiscalDateEnding"]) 
        bs["fiscalDateEnding"] = pd.to_datetime(bs["fiscalDateEnding"])
        prices_df = prices_df.sort_values("fiscalDateEnding", ascending=False)
        latest_closing_price = float(prices_df.iloc[0]["5. adjusted close"])
        
        def get_closest_adjusted_close(date):
            matching_row = prices_df[prices_df["fiscalDateEnding"] <= date].head(1)
            if not matching_row.empty:
                return float(matching_row["5. adjusted close"].iloc[0])
            return None
        
        bs["adjustedPrice"] = bs["fiscalDateEnding"].apply(get_closest_adjusted_close)
        bs["latest_closing_price"] = latest_closing_price
        bs["Symbol"] = ticker
        
        numeric_columns = ["commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "currentDebt"]
        for col in numeric_columns:
            bs[col] = pd.to_numeric(bs[col], errors="coerce")
            
        bs.fillna(0, inplace=True)
        
        latest_quarter_so = float(bs["commonStockSharesOutstanding"].iloc[0])
        latest_quarter_cash_cash_eq = float(bs["cashAndCashEquivalentsAtCarryingValue"].iloc[0])
        latest_quarter_current_debt = float(bs["currentDebt"].iloc[0])
        
        bs["mc"] = bs["commonStockSharesOutstanding"] * bs["adjustedPrice"]
        bs["currentmc"] = latest_quarter_so * latest_closing_price
        current_mc = bs["currentmc"]
        bs["ev"] = bs["mc"] + bs["cashAndCashEquivalentsAtCarryingValue"] + bs["currentDebt"]
        bs["latestev"] = current_mc + latest_quarter_cash_cash_eq + latest_quarter_current_debt
        
        result = bs[["fiscalDateEnding", "adjustedPrice", "latest_closing_price", "commonStockSharesOutstanding", 
                    "cashAndCashEquivalentsAtCarryingValue", "currentDebt", "currentmc", 
                    "latestev", "mc", "ev"]].copy()
        
        result = result.rename(columns={
            "commonStockSharesOutstanding": "sharesOutstanding",
            "cashAndCashEquivalentsAtCarryingValue": "cashCashEq",
            "currentmc": "latestMC"
        })
        
        if result.empty:
            raise HTTPException(status_code=404, detail="No results available after processing")
        
        return result.to_dict(orient="records")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

@router.get("/valuation/quarterly/{ticker}/ttm")
def get_valuation(ticker: str):
    try:
        summary = pd.DataFrame([get_summary(ticker)])
        symbol = summary.loc[0, "Symbol"]
        cap_struct_data = get_cap_struct(ticker)
        cap_struct = pd.DataFrame(cap_struct_data)
        ttm = pd.DataFrame(calculate_valuations(ticker))

        numeric_cols = [col for col in ttm.columns if col != "fiscalDateEnding"]
        for col in numeric_cols:
            ttm[col] = pd.to_numeric(ttm[col].str.replace(',', ''), errors="coerce")

        cap_struct = ensure_numeric(cap_struct)

        result = pd.DataFrame()
        result["fiscalDateEnding"] = cap_struct["fiscalDateEnding"]
        result["symbol"] = symbol

        def safe_division(numerator, denominator):
            result = (numerator / denominator).replace([np.inf, -np.inf], 0)
            return result.round(2)

        result["evtosales"] = safe_division(cap_struct["ev"], ttm["totalRevenue_ttm"])
        result["evtogrossprofit"] = safe_division(cap_struct["ev"], ttm["grossProfit_ttm"]) 
        result["evtoebit"] = safe_division(cap_struct["ev"], ttm["ebit_ttm"])
        result["evtoebitda"] = safe_division(cap_struct["ev"], ttm["ebitda_ttm"])
        result["evtonetincome"] = safe_division(cap_struct["ev"], ttm["netIncome_ttm"])
        result["revenue_per_share_ttm"] = safe_division(ttm["totalRevenue_ttm"], cap_struct["sharesOutstanding"])
        result["price_to_sales_ratio_ttm"] = safe_division(cap_struct["adjustedPrice"], result["revenue_per_share_ttm"])

        additional_metrics = ["AnalystTargetPrice", "AnalystRatingStrongBuy", "AnalystRatingBuy", 
                            "AnalystRatingHold", "AnalystRatingSell", "AnalystRatingStrongSell",
                            "TrailingPE", "ForwardPE", "Sector", "Industry"]

        for metric in additional_metrics:
            if metric in summary.columns:
                if metric in ["Sector", "Industry"]:
                    result[metric] = summary[metric].iloc[0]
                else:
                    value = summary[metric].iloc[0]
                    result[metric] = value if pd.notnull(value) else 0
                    result[metric] = pd.Series([value] * len(result), index=result.index)

        result = result.fillna(0)
        return result.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating valuations: {str(e)}")