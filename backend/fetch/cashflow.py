from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()


@router.get("/cashflow-statement/quarterly/{ticker}")
def get_quarterly_cashflow_statement_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")
    
    data_json = response.json()
    quarterly_reports = data_json.get("quarterlyReports", [])
    
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly cash flow data found")
    
    df = pd.DataFrame(quarterly_reports)
    
    numeric_columns = ["operatingCashflow", "capitalExpenditures"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    df["freeCashFlow"] = df["operatingCashflow"] - df["capitalExpenditures"]
    
    # Replace NaN and infinite values with 0
    df.replace([float("inf"), -float("inf"), pd.NA], 0, inplace=True)
    df.fillna(0, inplace=True)
    
    keys_to_exclude = [
        "reportedCurrency",
        "proceedsFromIssuanceOfCommonStock",
        "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet",
        "proceedsFromIssuanceOfPreferredStock",
        "proceedsFromSaleOfTreasuryStock",
        "changeInCashAndCashEquivalents",
        "changeInExchangeRate"
    ]
    transformed_reports = df.drop(columns=keys_to_exclude, errors="ignore")
    
    # Convert numeric columns to floats for JSON serialization
    transformed_reports = transformed_reports.astype({col: float for col in numeric_columns if col in transformed_reports.columns})
    
    result = transformed_reports.to_dict(orient="records")
    return result
