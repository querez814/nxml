from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data, get_annual_statement_data
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np

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
    income_df = pd.DataFrame(get_quarterly_statement_data(ticker))

    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in income_df.columns:
        if col != "fiscalDateEnding":
            income_df[col] = pd.to_numeric(income_df[col], errors="coerce")

    df["freeCashFlow"] = df["operatingCashflow"] - df["capitalExpenditures"]

    df.replace([np.inf, -np.inf, pd.NA], 0, inplace=True)
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
    df = df.drop(columns=keys_to_exclude, errors="ignore")

    df["net_profit_margin"] = (df["netIncome"] / df["operatingCashflow"]) * 100
    df["ocf_margin"] = (df["operatingCashflow"] / income_df["totalRevenue"]) * 100
    df["fcf_margin"] = (df["freeCashFlow"] / income_df["totalRevenue"]) * 100

    df["roce"] = df["netIncome"] / df["capitalExpenditures"]
    df["cash_flow_adequacy_ratio"] = df["operatingCashflow"] / (
        df["capitalExpenditures"] + df["dividendPayout"] + df["cashflowFromFinancing"]
    )
    df["capex_ratio"] = df["operatingCashflow"] / df["capitalExpenditures"]
    df["change_working_capital"] = df["changeInReceivables"] - df["changeInInventory"]

    ratio_cols = ["roce", "cash_flow_adequacy_ratio", "capex_ratio", "change_working_capital"]
    for col in ratio_cols:
        df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")

    margin_cols = ["net_profit_margin", "ocf_margin", "fcf_margin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [c for c in result_df.columns if c not in ["fiscalDateEnding"] + margin_cols + ratio_cols]

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]

    for col in numeric_cols:
        prev_4 = result_df[col].shift(4)
        prev_1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev_4) / prev_4.abs()) * 100
        qoq_series = ((result_df[col] - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        qoq_series = qoq_series.replace([np.inf, -np.inf], 0).fillna(0)

        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        change_df[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    for col in margin_cols + ratio_cols:
        temp_series = pd.to_numeric(result_df[col].str.replace("%", ""), errors="coerce")
        prev_4 = temp_series.shift(4)
        prev_1 = temp_series.shift(1)
        yoy_series = ((temp_series - prev_4) / prev_4.abs()) * 100
        qoq_series = ((temp_series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        qoq_series = qoq_series.replace([np.inf, -np.inf], 0).fillna(0)

        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
        change_df[f"{col}_QoQ"] = qoq_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")


@router.get("/cashflow-statement/annual/{ticker}")
def get_annual_cashflow_statement_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from Alpha Vantage")

    data_json = response.json()
    annual_reports = data_json.get("annualReports", [])
    if not annual_reports:
        raise HTTPException(status_code=404, detail="No quarterly cash flow data found")

    df = pd.DataFrame(annual_reports)
    income_df = pd.DataFrame(get_annual_statement_data(ticker))

    for col in df.columns:
        if col != "fiscalDateEnding":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in income_df.columns:
        if col != "fiscalDateEnding":
            income_df[col] = pd.to_numeric(income_df[col], errors="coerce")

    df["freeCashFlow"] = df["operatingCashflow"] - df["capitalExpenditures"]

    df.replace([np.inf, -np.inf, pd.NA], 0, inplace=True)
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
    df = df.drop(columns=keys_to_exclude, errors="ignore")

    df["net_profit_margin"] = (df["netIncome"] / df["operatingCashflow"]) * 100
    df["ocf_margin"] = (df["operatingCashflow"] / income_df["totalRevenue"]) * 100
    df["fcf_margin"] = (df["freeCashFlow"] / income_df["totalRevenue"]) * 100

    df["roce"] = df["netIncome"] / df["capitalExpenditures"]
    df["cash_flow_adequacy_ratio"] = df["operatingCashflow"] / (
        df["capitalExpenditures"] + df["dividendPayout"] + df["cashflowFromFinancing"]
    )
    df["capex_ratio"] = df["operatingCashflow"] / df["capitalExpenditures"]
    df["change_working_capital"] = df["changeInReceivables"] - df["changeInInventory"]

    ratio_cols = ["roce", "cash_flow_adequacy_ratio", "capex_ratio", "change_working_capital"]
    for col in ratio_cols:
        df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")

    margin_cols = ["net_profit_margin", "ocf_margin", "fcf_margin"]
    for col in margin_cols:
        df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    result_df = df.iloc[::-1].reset_index(drop=True)
    numeric_cols = [c for c in result_df.columns if c not in ["fiscalDateEnding"] + margin_cols + ratio_cols]

    change_df = pd.DataFrame()
    change_df["fiscalDateEnding"] = result_df["fiscalDateEnding"]

    for col in numeric_cols:
        prev_1 = result_df[col].shift(1)
        yoy_series = ((result_df[col] - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    for col in margin_cols + ratio_cols:
        temp_series = pd.to_numeric(result_df[col].str.replace("%", ""), errors="coerce")
        prev_1 = temp_series.shift(1)
        yoy_series = ((temp_series - prev_1) / prev_1.abs()) * 100
        yoy_series = yoy_series.replace([np.inf, -np.inf], 0).fillna(0)
        change_df[f"{col}_YoY"] = yoy_series.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    final_df = pd.merge(result_df, change_df, on="fiscalDateEnding")
    final_df = final_df.iloc[::-1].reset_index(drop=True)
    return final_df.to_dict(orient="records")
