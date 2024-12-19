from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
from fetch.earnings import get_quarterly_statement_data as earnings
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
    print("Quarterly Reports Extracted:", quarterly_reports)   
    quarterly_df = pd.DataFrame(quarterly_reports)
    earnings_df = pd.DataFrame(earnings(ticker))
    quarterly_df["reportedEPS"] = earnings_df["reportedEPS"]
    quarterly_df["estimatedEPS"] = earnings_df["estimatedEPS"]
    quarterly_df["surprise"] = earnings_df["surprise"]
    quarterly_df["surprisePercentage"] = earnings_df["surprisePercentage"]
    quarterly_reports = quarterly_df.to_dict(orient="records")
    keys_to_exclude = [
        'costofGoodsAndServicesSold', 'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]

    transformed_reports = [
        {
            "fiscalDateEnding": report.get("fiscalDateEnding", "N/A"),
            **{k: v for k, v in report.items() if k not in keys_to_exclude and k != "fiscalDateEnding"}
        }
        for report in quarterly_reports
    ]

    print("Transformed Reports:", transformed_reports)  

    return transformed_reports



