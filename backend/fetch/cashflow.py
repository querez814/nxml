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
    # Fetch data from Alpha Vantage API
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")
    
    data_json = response.json()
    quarterly_reports = data_json.get("quarterlyReports", [])
    
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly cash flow data found")
    
    # Create a DataFrame from quarterly reports
    df = pd.DataFrame(quarterly_reports)
    
    # Convert relevant columns to numeric for calculations
    df["operatingCashflow"] = pd.to_numeric(df["operatingCashflow"], errors="coerce")
    df["capitalExpenditures"] = pd.to_numeric(df["capitalExpenditures"], errors="coerce")
    
    # Calculate Free Cash Flow (FCF) and convert it to a string
    df["freeCashFlow"] = (df["operatingCashflow"] - df["capitalExpenditures"]).astype(str)
    
    # Exclude unwanted keys
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
    
    # Convert to list of dictionaries for JSON response
    result = transformed_reports.to_dict(orient="records")
    
    return result




print(get_quarterly_cashflow_statement_data("AMD"))