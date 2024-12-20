from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
from fetch.earnings import get_quarterly_earnings_data as earnings
import numpy as np
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

    # Convert to DataFrame
    quarterly_df = pd.DataFrame(quarterly_reports)

    # Ensure numerical columns are converted properly
    numeric_columns = [
        "totalRevenue", "grossProfit", "ebit", "ebitda", 
        "operatingIncome", "netIncome"
    ]
    for col in numeric_columns:
        quarterly_df[col] = pd.to_numeric(quarterly_df[col], errors="coerce")

  

  

    # Integrate earnings data
    earnings_df = pd.DataFrame(earnings(ticker))
    quarterly_df["reportedEPS"] = earnings_df["reportedEPS"]
    quarterly_df["estimatedEPS"] = earnings_df["estimatedEPS"]
    quarterly_df["surprise"] = earnings_df["surprise"]
    quarterly_df["surprisePercentage"] = earnings_df["surprisePercentage"]

    # Convert transformed reports back to dictionary
    keys_to_exclude = [
         'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]

    transformed_reports = [
        {
            "fiscalDateEnding": report.get("fiscalDateEnding", "N/A"),
            **{k: v for k, v in report.items() if k not in keys_to_exclude and k != "fiscalDateEnding"}
        }
        for report in quarterly_df.to_dict(orient="records")
    ]

    print("Transformed Reports:", transformed_reports)

    return transformed_reports



@router.get("/income-statement/quarterly/{ticker}/ttmmetrics")
def get_ttm_data(ticker: str):
    # Fetch the income statement data as a DataFrame
    income = pd.DataFrame(get_quarterly_statement_data(ticker))
    
    # Ensure numeric conversion for all columns except "fiscalDateEnding"
    for col in income.columns:
        if col != "fiscalDateEnding":
            income[col] = pd.to_numeric(income[col], errors="coerce")
    
    # Fill missing values with 0
    income = income.fillna(0)
    
    # Sort the DataFrame by fiscalDateEnding to ensure the most recent data is first
    income = income.sort_values(by="fiscalDateEnding", ascending=False)
    
    # Initialize a list to hold results
    result = []
    
    # Loop through each quarter to calculate both quarter metrics and TTM metrics
    for i in range(len(income)):
        quarter_data = income.iloc[i].to_dict()
        ttm_metrics = {}
        
        # Calculate TTM metrics for the most recent 4 quarters up to the current quarter
        for col in income.columns:
            if col != "fiscalDateEnding":
                # Ensure at least one quarter is included in TTM
                ttm_metrics[f"{col}_ttm"] = income[col].iloc[max(0, i):i + 4].sum()
        
        # Combine current quarter data with TTM metrics
        quarter_data.update(ttm_metrics)
        
        # Convert all numpy types to native Python types
        for key, value in quarter_data.items():
            if isinstance(value, (np.integer, np.floating)):
                quarter_data[key] = value.item()
        
        result.append(quarter_data)
    
    # Return JSON response
    return {"ticker": ticker, "quarters": result}
