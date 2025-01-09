from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()


@router.get("/balancesheet-statement/quarterly/{ticker}")
def get_quarterly_balance_sheet_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={av_api}"
    response = r.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")

    data_json = response.json()
    quarterly_reports = data_json.get("quarterlyReports", [])

    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly balance sheet data found")

    df = pd.DataFrame(quarterly_reports)
    
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)
    
    if "totalCurrentAssets" in df.columns and "totalCurrentLiabilities" in df.columns:
        df["working_capital"] = df["totalCurrentAssets"] - df["totalCurrentLiabilities"]
    else:
        df["working_capital"] = 0

    df["current_ratio"] = df["totalCurrentAssets"] / df["totalCurrentLiabilities"]
    df["quick_ratio"] = (df["totalCurrentAssets"] - df["inventory"]) / df["totalCurrentLiabilities"]
    df["cash_ratio"] = df["cashAndCashEquivalentsAtCarryingValue"] / df["totalCurrentLiabilities"]
    df["debt_to_equity_ratio"] = df["totalLiabilities"] / df["totalShareholderEquity"]
    df["debt_to_asset_ratio"] = df["totalLiabilities"] / df["totalAssets"]
    df["book_value_per_share"] = df["totalShareholderEquity"] / df["commonStockSharesOutstanding"]

    keys_to_include = [
        "fiscalDateEnding",
        "totalCurrentAssets",
        "totalAssets",
        "totalCurrentLiabilities",
        "totalLiabilities",
        "working_capital",
        "totalShareholderEquity",
        "commonStockSharesOutstanding",
        "cashAndCashEquivalentsAtCarryingValue",
        "inventory",
        "propertyPlantEquipment",
        "deferredRevenue",
        "currentDebt",
        "current_ratio",
        "quick_ratio",
        "cash_ratio",
        "debt_to_equity_ratio",
        "debt_to_asset_ratio",
        "book_value_per_share"
    ]

    result_df = df[keys_to_include] if set(keys_to_include).issubset(df.columns) else df
    result_df = result_df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col != "fiscalDateEnding"]
    
    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]
    
    for col in numeric_cols:
        if col in ["current_ratio", "quick_ratio", "cash_ratio", "debt_to_equity_ratio", "debt_to_asset_ratio", "book_value_per_share"]:
            result_df[col] = result_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")
            temp_series = pd.to_numeric(result_df[col], errors='coerce')
        else:
            temp_series = result_df[col]

        yoy_series = temp_series.pct_change(periods=4) * 100
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        
        qoq_series = temp_series.pct_change(periods=1) * 100
        change_df[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")

@router.get("/balancesheet-statement/annual/{ticker}")
def get_annual_balance_sheet_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={av_api}"
    response = r.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")

    data_json = response.json()
    annual_reports = data_json.get("annualReports", [])

    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly balance sheet data found")

    df = pd.DataFrame(annual_reports)
    
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)
    
    if "totalCurrentAssets" in df.columns and "totalCurrentLiabilities" in df.columns:
        df["working_capital"] = df["totalCurrentAssets"] - df["totalCurrentLiabilities"]
    else:
        df["working_capital"] = 0

    df["current_ratio"] = df["totalCurrentAssets"] / df["totalCurrentLiabilities"]
    df["quick_ratio"] = (df["totalCurrentAssets"] - df["inventory"]) / df["totalCurrentLiabilities"]
    df["cash_ratio"] = df["cashAndCashEquivalentsAtCarryingValue"] / df["totalCurrentLiabilities"]
    df["debt_to_equity_ratio"] = df["totalLiabilities"] / df["totalShareholderEquity"]
    df["debt_to_asset_ratio"] = df["totalLiabilities"] / df["totalAssets"]
    df["book_value_per_share"] = df["totalShareholderEquity"] / df["commonStockSharesOutstanding"]

    keys_to_include = [
        "fiscalDateEnding",
        "totalCurrentAssets",
        "totalAssets",
        "totalCurrentLiabilities",
        "totalLiabilities",
        "working_capital",
        "totalShareholderEquity",
        "commonStockSharesOutstanding",
        "cashAndCashEquivalentsAtCarryingValue",
        "inventory",
        "propertyPlantEquipment",
        "deferredRevenue",
        "currentDebt",
        "current_ratio",
        "quick_ratio",
        "cash_ratio",
        "debt_to_equity_ratio",
        "debt_to_asset_ratio",
        "book_value_per_share"
    ]

    result_df = df[keys_to_include] if set(keys_to_include).issubset(df.columns) else df
    result_df = result_df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col != "fiscalDateEnding"]
    
    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]
    
    for col in numeric_cols:
        if col in ["current_ratio", "quick_ratio", "cash_ratio", "debt_to_equity_ratio", "debt_to_asset_ratio", "book_value_per_share"]:
            result_df[col] = result_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")
            temp_series = pd.to_numeric(result_df[col], errors='coerce')
        else:
            temp_series = result_df[col]

        yoy_series = temp_series.pct_change(periods=1) * 100
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        
    
    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")
