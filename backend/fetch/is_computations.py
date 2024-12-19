from fastapi import APIRouter, HTTPException
import requests as r
from fetch.income_statement import get_quarterly_statement_data
import dotenv as env
import os
import json
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


@router.get("/income-statement/quarterly/{ticker}/margins")
def get_margins(ticker: str):
    result = pd.DataFrame(get_quarterly_statement_data(ticker))
    
    # Ensure numeric values for calculation
    for column in result.columns:
        if column != "fiscalDateEnding":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    # Calculate margins
    gross_margin = (result["grossProfit"] / result["totalRevenue"]) * 100
    operating_margin = (result["operatingIncome"] / result["totalRevenue"]) * 100
    ebit_margin = (result["ebit"] / result["totalRevenue"]) * 100
    ebitda_margin = (result["ebitda"] / result["totalRevenue"]) * 100
    net_margin = (result["netIncome"] / result["totalRevenue"]) * 100
    
    # Create a DataFrame for margins
    margin_df = pd.DataFrame({
        "fiscalDateEnding": result["fiscalDateEnding"],
        "grossMargin": gross_margin,
        "operatingMargin": operating_margin,
        "ebitMargin": ebit_margin,
        "ebitdaMargin": ebitda_margin,
        "netMargin": net_margin
    })
    
    # Calculate YoY growth for margins
    margin_df["grossMarginYoY"] = margin_df["grossMargin"].pct_change(periods=4) * 100
    margin_df["operatingMarginYoY"] = margin_df["operatingMargin"].pct_change(periods=4) * 100
    margin_df["ebitMarginYoY"] = margin_df["ebitMargin"].pct_change(periods=4) * 100
    margin_df["ebitdaMarginYoY"] = margin_df["ebitdaMargin"].pct_change(periods=4) * 100
    margin_df["netMarginYoY"] = margin_df["netMargin"].pct_change(periods=4) * 100
    
    # Handle NaN values and format as percentages
    for col in margin_df.columns:
        if col != "fiscalDateEnding":
            margin_df[col] = margin_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    # Convert DataFrame to JSON
    margin_df_json = margin_df.to_dict(orient="records")
    
    return margin_df_json