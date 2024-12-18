from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

@router.get("/income-statement/quarterly/{ticker}")
def get_quarterly_statement_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()

    print("Full API Response:", data_json)  # Debugging step

    # Extract the list of quarterly reports
    quarterly_reports = data_json.get("quarterlyReports", [])
    print("Quarterly Reports Extracted:", quarterly_reports)  # Debugging step

    # Keys to exclude
    keys_to_exclude = [
        'costofGoodsAndServicesSold', 'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]

    # Filter unwanted keys and add fiscalDateEnding as a field
    transformed_reports = [
        {
            "fiscalDateEnding": report.get("fiscalDateEnding", "N/A"),
            **{k: v for k, v in report.items() if k not in keys_to_exclude and k != "fiscalDateEnding"}
        }
        for report in quarterly_reports
    ]

    print("Transformed Reports:", transformed_reports)  # Debugging step

    return transformed_reports

