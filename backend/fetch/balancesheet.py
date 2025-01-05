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

    numeric_columns = [
        "totalCurrentAssets",
        "totalCurrentLiabilities",
        "totalAssets",
        "totalLiabilities",
        "totalShareholderEquity",
        "commonStockSharesOutstanding",
        "cashAndCashEquivalentsAtCarryingValue",
        "inventory",
        "propertyPlantEquipment",
        "deferredRevenue",
        "currentDebt"
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")  

    df.fillna(0, inplace=True)

    if "totalCurrentAssets" in df.columns and "totalCurrentLiabilities" in df.columns:
        df["workingCapital"] = df["totalCurrentAssets"] - df["totalCurrentLiabilities"]
    else:
        df["workingCapital"] = 0  

    keys_to_include = [
        "fiscalDateEnding",
        "totalCurrentAssets",
        "totalAssets",
        "totalCurrentLiabilities",
        "totalLiabilities",
        "workingCapital",
        "totalShareholderEquity",
        "commonStockSharesOutstanding",
        "cashAndCashEquivalentsAtCarryingValue",
        "inventory",
        "propertyPlantEquipment",
        "deferredRevenue",
        "currentDebt"
    ]

    result = df[keys_to_include] if set(keys_to_include).issubset(df.columns) else df

    json_result = result.to_dict(orient="records")
    return json_result


    
    
    
