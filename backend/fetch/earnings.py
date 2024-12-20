from fastapi import APIRouter, HTTPException

import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

@router.get("/earnings-statement/quarterly/{ticker}")
def get_quarterly_earnings_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()

    print("Full API Response:", data_json)  

    quarterly_reports = data_json.get("quarterlyEarnings", [])
    print("Quarterly Reports Extracted:", quarterly_reports)   




    return quarterly_reports 

    
    
    
    

@router.get("/earnings-statement/quarterly/{ticker}/yoy")
def get_yoy(ticker: str):
    result = pd.DataFrame(get_quarterly_earnings_data(ticker))
    
    for column in result.columns:
        if column != "reportedDate":
            result[column] = pd.to_numeric(result[column], errors="coerce")
    
    result = result.iloc[::-1].reset_index(drop=True)
    
    yoy_df = result.set_index("reportedDate").pct_change(periods=4, fill_method=None) * 100
 
    yoy_df.columns = [f"{col}_YoY" for col in yoy_df.columns]
    
    yoy_df = yoy_df.reset_index()
    yoy_df = yoy_df.iloc[::-1].reset_index(drop=True)
    
    yoy_df = yoy_df.fillna(0)
    
    for col in yoy_df.columns:
        if col != "reportedDate":
            yoy_df[col] = yoy_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "0.0%")
    
    yoy_json = yoy_df.to_dict(orient="records")
    
    return yoy_json



