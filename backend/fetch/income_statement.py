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
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")
    data_json = response.json()
    quarterly_reports = data_json.get("quarterlyReports", [])
    if not quarterly_reports:
        raise HTTPException(status_code=404, detail="No quarterly reports found.")
    df = pd.DataFrame(quarterly_reports)
    earnings_df = pd.DataFrame(earnings(ticker))
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]:
        earnings_df[col] = pd.to_numeric(earnings_df[col], errors="coerce")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.replace([np.inf, -np.inf, np.nan], 0)

    earnings_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    earnings_df = earnings_df.replace([np.inf, -np.inf, np.nan], 0)

    df["reportedEPS"] = earnings_df["reportedEPS"]
    df["estimatedEPS"] = earnings_df["estimatedEPS"]
    df["surprise"] = earnings_df["surprise"]
    df["surprisePercentage"] = earnings_df["surprisePercentage"]
    keys_to_exclude = [
        'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]
    df = df.drop(columns=keys_to_exclude, errors='ignore')
    df["grossMargin"] = (df["grossProfit"] / df["totalRevenue"]) * 100
    df["operatingMargin"] = (df["operatingIncome"] / df["totalRevenue"]) * 100
    df["ebitMargin"] = (df["ebit"] / df["totalRevenue"]) * 100
    df["ebitdaMargin"] = (df["ebitda"] / df["totalRevenue"]) * 100
    df["netMargin"] = (df["netIncome"] / df["totalRevenue"]) * 100
    margin_cols = ["grossMargin", "operatingMargin", "ebitMargin", "ebitdaMargin", "netMargin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col not in ["fiscalDateEnding"] + margin_cols]
    changes_list = []
    for col in numeric_cols:
        temp_dict = {"fiscalDateEnding": result_df["fiscalDateEnding"]}
        prev4 = result_df[col].shift(4)
        prev1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev4) / prev4.abs()) * 100
        qoq_series = ((result_df[col] - prev1) / prev1.abs()) * 100
        yoy_derivative = ((yoy_series - yoy_series.shift(1)) / yoy_series.shift(1).abs()) * 100
        qoq_derivative = ((qoq_series - qoq_series.shift(1)) / qoq_series.shift(1).abs()) * 100
        temp_dict[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        temp_dict[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        temp_dict[f"{col}_YoY_Derivative"] = yoy_derivative.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        temp_dict[f"{col}_QoQ_Derivative"] = qoq_derivative.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        changes_list.append(pd.DataFrame(temp_dict))
    for col in margin_cols:
        temp_dict = {"fiscalDateEnding": result_df["fiscalDateEnding"]}
        numeric_margin = pd.to_numeric(result_df[col].str.replace('%', ''), errors='coerce')
        prev4_margin = numeric_margin.shift(4)
        prev1_margin = numeric_margin.shift(1)
        yoy_series = ((numeric_margin - prev4_margin) / prev4_margin.abs()) * 100
        qoq_series = ((numeric_margin - prev1_margin) / prev1_margin.abs()) * 100
        yoy_derivative = ((yoy_series - yoy_series.shift(1)) / yoy_series.shift(1).abs()) * 100
        qoq_derivative = ((qoq_series - qoq_series.shift(1)) / qoq_series.shift(1).abs()) * 100
        temp_dict[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        temp_dict[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        temp_dict[f"{col}_YoY_Derivative"] = yoy_derivative.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        temp_dict[f"{col}_QoQ_Derivative"] = qoq_derivative.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        changes_list.append(pd.DataFrame(temp_dict))
    all_changes = changes_list[0]
    for df_change in changes_list[1:]:
        all_changes = pd.merge(all_changes, df_change, on="fiscalDateEnding")
    final_df = pd.merge(result_df, all_changes, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    final_df = final_df.replace([np.inf, -np.inf, np.nan], 0)
    return final_df.to_dict(orient="records")

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
                ttm_metrics[f"{col}TTM"] = income[col].iloc[max(0, i):i + 4].sum()
        quarter_data.update(ttm_metrics)
        for key, value in quarter_data.items():
            if isinstance(value, (np.integer, np.floating)):
                quarter_data[key] = value.item()
        result.append(quarter_data)
    return {"ticker": ticker, "quarters": result}

@router.get("/income-statement/annual/{ticker}")
def get_annual_statement_data(ticker:str):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")
    data_json = response.json()
    annual_reports = data_json.get("annualReports", [])
    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly reports found.")
    df = pd.DataFrame(annual_reports)
    earnings_df = pd.DataFrame(earnings(ticker))
    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]:
        earnings_df[col] = pd.to_numeric(earnings_df[col], errors="coerce")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)
    earnings_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    earnings_df.fillna(0, inplace=True)
    df["reportedEPS"] = earnings_df["reportedEPS"]
    df["estimatedEPS"] = earnings_df["estimatedEPS"]
    df["surprise"] = earnings_df["surprise"]
    df["surprisePercentage"] = earnings_df["surprisePercentage"]
    keys_to_exclude = [
        'reportedCurrency', 'investmentIncomeNet',
        'netInterestIncome', 'nonInterestIncome', 'otherNonOperatingIncome',
        'depreciation', 'depreciationAndAmortization',
        'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax'
    ]
    df = df.drop(columns=keys_to_exclude, errors='ignore')
    df["grossMargin"] = (df["grossProfit"] / df["totalRevenue"]) * 100
    df["operatingMargin"] = (df["operatingIncome"] / df["totalRevenue"]) * 100
    df["ebitMargin"] = (df["ebit"] / df["totalRevenue"]) * 100
    df["ebitdaMargin"] = (df["ebitda"] / df["totalRevenue"]) * 100
    df["netMargin"] = (df["netIncome"] / df["totalRevenue"]) * 100
    margin_cols = ["grossMargin", "operatingMargin", "ebitMargin", "ebitdaMargin", "netMargin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [col for col in result_df.columns if col not in ["fiscalDateEnding"] + margin_cols]
    changes_list = []
    for col in numeric_cols:
        temp_dict = {"fiscalDateEnding": result_df["fiscalDateEnding"]}
        prev1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev1) / prev1.abs()) * 100
        temp_dict[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        changes_list.append(pd.DataFrame(temp_dict))
    for col in margin_cols:
        temp_dict = {"fiscalDateEnding": result_df["fiscalDateEnding"]}
        numeric_margin = pd.to_numeric(result_df[col].str.replace('%', ''), errors='coerce')
        prev1_margin = numeric_margin.shift(1)
        yoy_series = ((numeric_margin - prev1_margin) / prev1_margin.abs()) * 100
        temp_dict[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        changes_list.append(pd.DataFrame(temp_dict))
    all_changes = changes_list[0]
    for df_change in changes_list[1:]:
        all_changes = pd.merge(all_changes, df_change, on="fiscalDateEnding")
    final_df = pd.merge(result_df, all_changes, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")
