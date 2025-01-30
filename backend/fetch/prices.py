from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data
from fetch.cashflow import get_quarterly_cashflow_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/prices/{ticker}")
def get_prices(ticker: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()
    
    time_series = data_json.get("Time Series (Daily)", {})
    transformed_data = []

    for date, values in time_series.items():
        flattened_entry = {"fiscalDateEnding": date}
        for key, value in values.items():
            try:
                flattened_entry[key] = round(float(value), 2)  
            except ValueError:
                
                flattened_entry[key] = 0  
        transformed_data.append(flattened_entry)

    prices_df = pd.DataFrame(transformed_data)

    return prices_df.to_dict(orient="records")


@router.get("/close/{ticker}")
def get_closing_prices(ticker:str):
    prices = get_prices(ticker)
    prices_df = pd.DataFrame(prices)
    closing_prices = prices_df["4. close"]
    closing_prices.to_list()
    closing_list = []
    for key in closing_prices:
        closing_list.append(
           key 
            
        )

        
    return closing_list 
def candlesticks():
    return  