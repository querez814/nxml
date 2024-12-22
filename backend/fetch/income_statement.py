from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np

from fetch.earnings import get_quarterly_earnings_data as earnings

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

@router.get("/income-statement/quarterly/{ticker}")
def get_quarterly_statement_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()

    print("Full API Response:", data_json)

    quarterly_reports = data_json.get("quarterlyReports", [])
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly reports found.")

    quarterly_df = pd.DataFrame(quarterly_reports)

    numeric_columns = [
        "totalRevenue", "grossProfit", "ebit", "ebitda", 
        "operatingIncome", "netIncome"
    ]
    for col in numeric_columns:
        quarterly_df[col] = pd.to_numeric(quarterly_df[col], errors="coerce")

    quarterly_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    quarterly_df.fillna(0, inplace=True)

    earnings_df = pd.DataFrame(earnings(ticker))
    for col in ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]:
        earnings_df[col] = pd.to_numeric(earnings_df[col], errors="coerce")

    earnings_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    earnings_df.fillna(0, inplace=True)

    quarterly_df["reportedEPS"] = earnings_df["reportedEPS"]
    quarterly_df["estimatedEPS"] = earnings_df["estimatedEPS"]
    quarterly_df["surprise"] = earnings_df["surprise"]
    quarterly_df["surprisePercentage"] = earnings_df["surprisePercentage"]

    keys_to_exclude = [
        'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]

    transformed_reports = []
    for report in quarterly_df.to_dict(orient="records"):
        filtered_report = {
            "fiscalDateEnding": report.get("fiscalDateEnding", "N/A"),
            **{k: v for k, v in report.items() if k not in keys_to_exclude and k != "fiscalDateEnding"}
        }

        cleaned_report = {
            k: (None if pd.isna(v) else float(v) if isinstance(v, (int, float, np.number)) else v)
            for k, v in filtered_report.items()
        }
        transformed_reports.append(cleaned_report)

    print("Transformed Reports:", transformed_reports)

    return transformed_reports


from fastapi.responses import JSONResponse

@router.get("/income-statement/quarterly/{ticker}/ttmmetrics")
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
                ttm_metrics[f"{col}_ttm"] = income[col].iloc[max(0, i):i + 4].sum()
        
        quarter_data.update(ttm_metrics)
        
        for key, value in quarter_data.items():
            if isinstance(value, (np.integer, np.floating)):
                quarter_data[key] = value.item()
        
        result.append(quarter_data)
    
    return {"ticker": ticker, "quarters": result}
