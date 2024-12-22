
from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data 
from fetch.cashflow import get_quarterly_cashflow_statement_data
import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/cashflow-statement/quarterly/{ticker}/margins")
def get_cf_margins(ticker:str):
    income = pd.DataFrame(get_quarterly_statement_data(ticker))

    for col in income.columns:
        if col!="fiscalDateEnding":
            income[col] = pd.to_numeric(income[col], errors="coerce")
    
    cash_flow = pd.DataFrame(get_quarterly_cashflow_statement_data(ticker))
    for col in cash_flow.columns:
        if col!="fiscalDateEnding":
            cash_flow[col] = pd.to_numeric(cash_flow[col], errors="coerce")
    
    
    net_profit_margin =(cash_flow["netIncome"]/cash_flow["operatingCashflow"])*100
    ocf_margin =  (cash_flow["operatingCashflow"]/income["totalRevenue"])*100   
    fcf_margin = (cash_flow["freeCashFlow"]/income["totalRevenue"])*100
    capex_ratio = (cash_flow["operatingCashflow"]/cash_flow["capitalExpenditures"])
    cf_margin_df = pd.DataFrame({
        "fiscalDateEnding": income["fiscalDateEnding"],
        "net_profit_margin":net_profit_margin,
        "ocf_margin": ocf_margin,
        "fcf_margin":fcf_margin,
    })

    
    cf_margin_df = cf_margin_df.fillna(0)
    for col in cf_margin_df.columns:
        if col!="fiscalDateEnding":
            
            cf_margin_df[col] = cf_margin_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
            
    cf_margin_df_json = cf_margin_df.to_dict(orient="records")
    
    return cf_margin_df_json

@router.get("/cashflow-statement/quarterly/{ticker}/margins/yoy")
def get_cf_margins_yoy(ticker: str):
    cf = pd.DataFrame(get_cf_margins(ticker))

    for col in ["net_profit_margin", "ocf_margin", "fcf_margin"]:
        cf[col] = cf[col].str.replace("%", "").astype(float)

    cf = cf.iloc[::-1].reset_index(drop=True)

    cf_ratios_yoy = cf.set_index("fiscalDateEnding").pct_change(periods=4, fill_method=None) * 100

    cf_ratios_yoy.columns = [f"{col}_YoY" for col in cf_ratios_yoy.columns]

    cf_ratios_yoy = cf_ratios_yoy.reset_index()
    cf_ratios_yoy = cf_ratios_yoy[::-1].reset_index(drop=True)

    cf_ratios_yoy = cf_ratios_yoy.fillna(0)

    for col in cf_ratios_yoy.columns:
        if col != "fiscalDateEnding":
            cf_ratios_yoy[col] = cf_ratios_yoy[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    cf_ratios_yoy_json = cf_ratios_yoy.to_dict(orient="records")

    return cf_ratios_yoy_json


@router.get("/cashflow-statement/quarterly/{ticker}/margins/qoq")
def get_cf_margins_qoq(ticker: str):
    cf = pd.DataFrame(get_cf_margins(ticker))

    for col in ["net_profit_margin", "ocf_margin", "fcf_margin"]:
        cf[col] = cf[col].str.replace("%", "").astype(float)

    cf = cf.iloc[::-1].reset_index(drop=True)

    cf_ratios_qoq = cf.set_index("fiscalDateEnding").pct_change(periods=4, fill_method=None) * 100

    cf_ratios_qoq.columns = [f"{col}_QoQ" for col in cf_ratios_qoq.columns]

    cf_ratios_qoq = cf_ratios_qoq.reset_index()
    cf_ratios_qoq = cf_ratios_qoq[::-1].reset_index(drop=True)

    cf_ratios_qoq = cf_ratios_qoq.fillna(0)

    for col in cf_ratios_qoq.columns:
        if col != "fiscalDateEnding":
            cf_ratios_qoq[col] = cf_ratios_qoq[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")

    cf_ratios_qoq_json = cf_ratios_qoq.to_dict(orient="records")

    return cf_ratios_qoq_json


@router.get("/cashflow-statement/quarterly/{ticker}/ratios")
def get_cf_ratios(ticker:str):
    income = pd.DataFrame(get_quarterly_statement_data(ticker))
    
    for col in income.columns:
        if col!="fiscalDateEnding":
            income[col] = pd.to_numeric(income[col],errors="coerce")
    
    
    cash_flow = pd.DataFrame(get_quarterly_cashflow_statement_data(ticker))
    for col in cash_flow.columns:
        if col!="fiscalDateEnding":
            cash_flow[col] = pd.to_numeric(cash_flow[col], errors="coerce")

    roce =(cash_flow["netIncome"]/cash_flow["capitalExpenditures"])
    cash_flow_adequacy_ratio = (cash_flow["operatingCashflow"]/(cash_flow["capitalExpenditures"]+cash_flow["dividendPayout"]+cash_flow["cashflowFromFinancing"]))
    capex_ratio =(cash_flow["operatingCashflow"]/cash_flow["capitalExpenditures"])
    delta_working_capital =cash_flow["changeInReceivables"]-cash_flow["changeInInventory"]
    cf_ratio_df = pd.DataFrame({
        "fiscalDateEnding":cash_flow["fiscalDateEnding"],
        "roce":roce,
        "cfa_ratio": cash_flow_adequacy_ratio,
        "capex_ratio":capex_ratio,
        "change_working_capital":delta_working_capital
    })

    cf_ratio_df = cf_ratio_df.fillna(0)
    
    for col in cf_ratio_df.columns:
        if col!="fiscalDateEnding":
            cf_ratio_df[col] = cf_ratio_df[col].apply(lambda x:f"{x:.2f}" if pd.notnull else "0.0")

            
    cf_ratio_df_json = cf_ratio_df.to_dict(orient="records")

    return cf_ratio_df_json

@router.get("/cashflow-statement/quarterly/{ticker}/ratios/yoy")
def get_cf_ratios_yoy(ticker:str):
    cf = pd.DataFrame(get_cf_ratios(ticker))
    
    for col in cf.columns:
        if col != "fiscalDateEnding":
            cf[col]=pd.to_numeric(cf[col],errors="coerce")
            
    cf = cf.iloc[::-1].reset_index(drop=True)
    
    cf_ratios_yoy = cf.set_index("fiscalDateEnding").pct_change(periods=4,fill_method=None)*100
    
    cf_ratios_yoy.columns=[f"{col}_YoY" for col in cf_ratios_yoy.columns]         

    cf_ratios_yoy.reset_index()
    cf_ratios_yoy = cf_ratios_yoy[::-1].reset_index(drop=True)
    
    cf_ratios_yoy = cf_ratios_yoy.fillna(0)
    
    for col in cf_ratios_yoy.columns:
        if col !="fiscalDateEnding":
            cf_ratios_yoy[col]=cf_ratios_yoy[col].apply(lambda x:f"{x:.1f}%" if pd.notnull(x) else "0.0%")
            
            
    cf_ratios_yoy_json = cf_ratios_yoy.to_dict(orient="records")
    
    return cf_ratios_yoy_json
@router.get("/cashflow-statement/quarterly/{ticker}/ratios/qoq")
def get_cf_ratios_qoq(ticker:str):
    cf = pd.DataFrame(get_cf_ratios(ticker))
    
    for col in cf.columns:
        if col != "fiscalDateEnding":
            cf[col]=pd.to_numeric(cf[col],errors="coerce")
            
    cf = cf.iloc[::-1].reset_index(drop=True)
    
    cf_ratios_qoq = cf.set_index("fiscalDateEnding").pct_change(periods=1,fill_method=None)*100
    
    cf_ratios_qoq.columns=[f"{col}_QoQ" for col in cf_ratios_qoq.columns]         

    cf_ratios_qoq.reset_index()
    cf_ratios_qoq = cf_ratios_qoq[::-1].reset_index(drop=True)
    
    cf_ratios_qoq = cf_ratios_qoq.fillna(0)
    
    for col in cf_ratios_qoq.columns:
        if col !="fiscalDateEnding":
            cf_ratios_qoq[col]=cf_ratios_qoq[col].apply(lambda x:f"{x:.1f}%" if pd.notnull(x) else "0.0%")
            
            
    cf_ratios_yoy_json = cf_ratios_qoq.to_dict(orient="records")
    
    return cf_ratios_yoy_json
@router.get("/cashflow-statement/quarterly/{ticker}/yoy")
def get_yoy(ticker: str):
    result = pd.DataFrame(get_quarterly_cashflow_statement_data(ticker))
    
    for column in result.columns:
        if column != "fiscalDateEnding":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    result = result.iloc[::-1].reset_index(drop=True)
    
    yoy_df = result.set_index("fiscalDateEnding").pct_change(periods=4, fill_method=None) * 100
 
    yoy_df.columns = [f"{col}_YoY" for col in yoy_df.columns]
    
    yoy_df = yoy_df.reset_index()
    yoy_df = yoy_df.iloc[::-1].reset_index(drop=True)
    
    yoy_df = yoy_df.fillna(0)
    
    for col in yoy_df.columns:
        if col != "fiscalDateEnding":
            
            yoy_df[col] = yoy_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    yoy_json = yoy_df.to_dict(orient="records")
    
    return yoy_json




@router.get("/cashflow-statement/quarterly/{ticker}/qoq")
def get_qoq(ticker: str):
    result = pd.DataFrame(get_quarterly_cashflow_statement_data(ticker))
    
    for column in result.columns:
        if column != "fiscalDateEnding":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    result = result.iloc[::-1].reset_index(drop=True)
    
    yoy_df = result.set_index("fiscalDateEnding").pct_change(periods=1, fill_method=None) * 100
 
    yoy_df.columns = [f"{col}_QoQ" for col in yoy_df.columns]
    
    yoy_df = yoy_df.reset_index()
    yoy_df = yoy_df.iloc[::-1].reset_index(drop=True)
    
    yoy_df = yoy_df.fillna(0)
    
    for col in yoy_df.columns:
        if col != "fiscalDateEnding":
            yoy_df[col] = yoy_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    yoy_json = yoy_df.to_dict(orient="records")
    
    return yoy_json
