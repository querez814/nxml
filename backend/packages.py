from fastapi import APIRouter, HTTPException
from fetch.prices import get_prices
from fetch.income_statement import get_quarterly_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()



@router.get("/summary/{ticker}")
def get_summary(ticker:str):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()
    return data_json


def get_ttm_data(ticker: str):
    quarterly_data = get_quarterly_statement_data(ticker)
    income = pd.DataFrame(quarterly_data)
    
    for col in income.columns:
        if col != "fiscalDateEnding":
            income[col] = pd.to_numeric(income[col], errors="coerce")
    
    income = income.fillna(0)
    income = income.sort_values(by="fiscalDateEnding", ascending=False)
    
    result = []
    for i in range(len(income)):
        quarter_data = income.iloc[i].to_dict()
        ttm_metrics = {}
        
        for col in income.columns:
            if col != "fiscalDateEnding":
                ttm_metrics[f"{col}TTM"] = income[col].iloc[max(0, i):i + 4].sum()
        
        quarter_data.update(ttm_metrics)
        
        for key, value in quarter_data.items():
            if isinstance(value, (np.integer, np.floating)):
                quarter_data[key] = value.item()
        
        result.append(quarter_data)
    
    return {"ticker": ticker, "quarters": result}

def ensure_numeric(df, exclude_cols=["fiscalDateEnding", "Symbol"]):
    for col in df.columns:
        if col not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.fillna(0)

@router.get("/capitalstructure/quarterly/{ticker}")
async def get_cap_struct(ticker: str):
    
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
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

   try:
       prices_df["fiscalDateEnding"] = pd.to_datetime(prices_df["fiscalDateEnding"]) 
       bs["fiscalDateEnding"] = pd.to_datetime(bs["fiscalDateEnding"])
       prices_df = prices_df.sort_values("fiscalDateEnding", ascending=False)
       latest_closing_price = float(prices_df.iloc[0]["5. adjusted close"])
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error processing dates or prices: {str(e)}")

   def get_closest_adjusted_close(date):
       matching_row = prices_df[prices_df["fiscalDateEnding"] <= date].head(1)
       if not matching_row.empty:
           return float(matching_row["5. adjusted close"].iloc[0])
       return None

   try:
       bs["adjustedPrice"] = bs["fiscalDateEnding"].apply(get_closest_adjusted_close)
       bs["latest_closing_price"] = latest_closing_price
       
       bs["Symbol"] = ticker
       
       numeric_columns = ["commonStockSharesOutstanding", "cashAndCashEquivalentsAtCarryingValue", "currentDebt"]
       for col in numeric_columns:
           bs[col] = pd.to_numeric(bs[col], errors="coerce")
           
       bs.fillna(0, inplace=True)
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error matching prices to dates: {str(e)}")

   try:
       latest_quarter_so = float(bs["commonStockSharesOutstanding"].iloc[0])
       latest_quarter_cash_cash_eq = float(bs["cashAndCashEquivalentsAtCarryingValue"].iloc[0])
       latest_quarter_current_debt = float(bs["currentDebt"].iloc[0])
    
       bs["mc"] = bs["commonStockSharesOutstanding"] * bs["adjustedPrice"]
       bs["currentmc"] = latest_quarter_so * latest_closing_price
       current_mc = bs["currentmc"]
       bs["ev"] = bs["mc"] + bs["cashAndCashEquivalentsAtCarryingValue"] + bs["currentDebt"]
       bs["latestev"] = current_mc + latest_quarter_cash_cash_eq + latest_quarter_current_debt
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error calculating metrics: {str(e)}")

   try:
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
       raise HTTPException(status_code=500, detail=f"Error preparing final output: {str(e)}")

@router.get("/valuation/{ticker}/ttm")
async def get_valuation(ticker: str):
    summary = pd.DataFrame([get_summary(ticker)])
    symbol = summary.loc[0, "Symbol"]

    cap_struct_data = await get_cap_struct(ticker)
    cap_struct = pd.DataFrame(cap_struct_data)
    ttm = pd.DataFrame(calculate_valuations(ticker))

    numeric_cols = [col for col in ttm.columns if col != "fiscalDateEnding"]
    for col in numeric_cols:
        ttm[col] = pd.to_numeric(ttm[col].str.replace(',', ''), errors='coerce')

    cap_struct["Symbol"] = symbol
    cap_struct = ensure_numeric(cap_struct)

    result = pd.DataFrame()
    result["fiscalDateEnding"] = cap_struct["fiscalDateEnding"]
    result["symbol"] = symbol

    result["evtosales"] = (cap_struct["ev"] / ttm["totalRevenue_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtogrossprofit"] = (cap_struct["ev"] / ttm["grossProfit_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtoebit"] = (cap_struct["ev"] / ttm["ebit_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtoebitda"] = (cap_struct["ev"] / ttm["ebitda_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["evtonetincome"] = (cap_struct["ev"] / ttm["netIncome_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["revenue_per_share_ttm"] = (ttm["totalRevenue_ttm"] / cap_struct["sharesOutstanding"]).replace([np.inf, -np.inf], 0).round(2)
    result["price_to_sales_ratio_ttm"] = (cap_struct["adjustedPrice"] / result["revenue_per_share_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["current_evtosales_ttm"] = (cap_struct["latestev"] / ttm["totalRevenue_ttm"]).replace([np.inf, -np.inf], 0).round(2)
    result["current_price_to_sales_ratio_ttm"] = (cap_struct["latest_closing_price"] / result["revenue_per_share_ttm"]).replace([np.inf, -np.inf], 0).round(2)

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

@router.get("/valuation/quarterly/{ticker}")
def calculate_valuations(ticker:str):
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