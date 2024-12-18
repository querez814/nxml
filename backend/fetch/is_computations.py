from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data
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

@router.get("/income-statement/quarterly/{ticker}/yoy")
def get_yoy(ticker: str):
    # Fetch the quarterly data for the given ticker
    result = pd.DataFrame(get_quarterly_statement_data(ticker))
    
    # Ensure numeric values for calculation, except for the "fiscalDateEnding" column
    for column in result.columns:
        if column != "fiscalDateEnding":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    # Reverse the DataFrame order for chronological calculations
    result = result.iloc[::-1].reset_index(drop=True)
    
    # Calculate Year-over-Year percentage change (4 quarters apart)
    yoy_df = result.set_index("fiscalDateEnding").pct_change(periods=4, fill_method=None) * 100
 
    # Format column names to indicate YoY values
    yoy_df.columns = [f"{col}_YoY" for col in yoy_df.columns]
    
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

@router.get("/income-statement/quarterly/{ticker}/qoq")
def get_qoq(ticker: str):
    # Fetch the quarterly data for the given ticker
    result = pd.DataFrame(get_quarterly_statement_data(ticker))
    
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
