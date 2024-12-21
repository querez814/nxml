

from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data
from fetch.cashflow import get_quarterly_cashflow_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/balancesheet-statement/quarterly/{ticker}/ratios")
def bs_ratios(ticker:str):
    bs = pd.DataFrame(get_quarterly_balance_sheet_data(ticker))
    is_df = pd.DataFrame(get_quarterly_statement_data(ticker))
    
    for col in is_df.columns:
        if col != "fiscalDateEnding":
            is_df[col] = pd.to_numeric(is_df[col], errors="coerce")
    
    for col in bs.columns:
        if col != "fiscalDateEnding":
            bs[col] = pd.to_numeric(bs[col], errors="coerce")
            
    current_ratio = (bs["totalCurrentAssets"]/bs["totalCurrentLiabilities"])
    quick_ratio = ((bs["totalCurrentAssets"]-bs["inventory"])/(bs["totalCurrentLiabilities"])) 
    cash_ratio =(bs["cashAndCashEquivalentsAtCarryingValue"]/(bs["totalCurrentLiabilities"]))
    debt_to_equity_ratio=(bs["totalLiabilities"]/bs["totalShareholderEquity"])
    debt_to_asset_ratio =(bs["totalLiabilities"]/bs["totalAssets"])
    inventory_turnover = (is_df["costofGoodsAndServicesSold"]/bs["inventory"])
    roa = (is_df["netIncome"]/bs["totalAssets"])
    roe= (is_df["netIncome"]/bs["totalShareholderEquity"])
    book_value_per_share = (bs["totalShareholderEquity"]/bs["commonStockSharesOutstanding"])
    
    bs_ratios_df= pd.DataFrame({
        "fiscalDateEnding":bs["fiscalDateEnding"],
        "current_ratio":current_ratio,
        "quick_ratio":quick_ratio,
        "cash_ratio" : cash_ratio,
        "debt_to_equity_ratio":debt_to_equity_ratio,
        "debt_to_asset_ratio":debt_to_asset_ratio,
        "inventory_turnover_ratio": inventory_turnover,
        "roa":roa,
        "roe":roe,
        "book_value_per_share":book_value_per_share
    })
    
    bs_ratios_df= bs_ratios_df.fillna(0)
    for col in bs_ratios_df.columns:
        if col!="fiscalDateEnding":
            bs_ratios_df[col] = bs_ratios_df[col].apply(lambda x:f"{x:.2f}" if pd.notnull(x) else"0")
            
    bs_ratios_json = bs_ratios_df.to_dict(orient="records")
    
    return bs_ratios_json




@router.get("/balancesheet-statement/quarterly/{ticker}/yoy")
def get_yoy(ticker: str):
    result = pd.DataFrame(get_quarterly_balance_sheet_data(ticker))
    
    for column in result.columns:
        if column != "fiscalDateEnding":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    result = result.iloc[::-1].reset_index(drop=True)
    
    yoy_df = result.set_index("fiscalDateEnding").pct_change(periods=4, fill_method=None) * 100
 
    yoy_df.columns = [f"{col}_YoY" for col in yoy_df.columns]
    
    yoy_df = yoy_df.reset_index()
    yoy_df = yoy_df.iloc[::-1].reset_index(drop=True)
    
    yoy_df = yoy_df.fillna(0)
    
    for col in yoy_df.columns:
        if col != "fiscalDateEnding":
            yoy_df[col] = yoy_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    yoy_json = yoy_df.to_dict(orient="records")
    
    return yoy_json





@router.get("/balancesheet-statement/quarterly/{ticker}/qoq")
def get_qoq(ticker: str):
    # Fetch the quarterly data for the given ticker
    result = pd.DataFrame(get_quarterly_balance_sheet_data(ticker))
    
    # Ensure numeric values for calculation, except for the "fiscalDateEnding" column
    for column in result.columns:
        if column != "fiscalDateEnding":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    # Reverse the DataFrame order for chronological calculations
    result = result.iloc[::-1].reset_index(drop=True)
    
    # Calculate Year-over-Year percentage change (4 quarters apart)
    yoy_df = result.set_index("fiscalDateEnding").pct_change(periods=1, fill_method=None) * 100
 
    # Format column names to indicate YoY values
    yoy_df.columns = [f"{col}_QoQ" for col in yoy_df.columns]
    
    # Reset index to include "fiscalDateEnding" and reverse order for display
    yoy_df = yoy_df.reset_index()
    yoy_df = yoy_df.iloc[::-1].reset_index(drop=True)
    
    # Handle NaN values by filling with 0 (optional: drop rows with NaN values instead)
    yoy_df = yoy_df.fillna(0)
    
    # Format YoY values as percentages
    for col in yoy_df.columns:
        if col != "fiscalDateEnding":
            yoy_df[col] = yoy_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    # Convert DataFrame to JSON for API response
    yoy_json = yoy_df.to_dict(orient="records")
    
    return yoy_json
