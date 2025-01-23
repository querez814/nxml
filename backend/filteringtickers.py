from fastapi import APIRouter, HTTPException 
from fetch.prices import get_prices
import dotenv as env
import os
import numpy as np
import pandas as pd
import requests as r

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

columns = ['symbol', 'name']

"""
@router.get("/beta/")
def get_ticker_beta():
    high_beta_stocks = []
    
    for ticker in ticker_list:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={av_api}"
        response = r.get(url)
        data_json = response.json()
        
        if "Beta" not in data_json:
            continue
            
        try:
            beta = float(data_json["Beta"])
            if beta > 2: 
                high_beta_stocks.append({
                    "ticker": ticker,
                    "beta": beta
                })
                
        except ValueError:
            continue
    
    sorted_stocks = sorted(high_beta_stocks, key=lambda x: x['beta'], reverse=True)
    
    return sorted_stocks
    
@router.get("/gainers")    
def top_gainers():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={av_api}"
    requests = r.get(url)
    data_json = requests.json()
    top_gainers = data_json["top_gainers"]

    return top_gainers 



@router.get("/losers")
def top_losers():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={av_api}"
    requests = r.get(url)
    data_json = requests.json()
    top_losers = data_json["top_losers"]

    return top_losers



@router.get("/mosttraded")
def most_traded():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={av_api}"
    requests = r.get(url)
    data_json = requests.json()
    most_traded = data_json["most_actively_traded"]

    return most_traded

    
@router.get("/cgl")    
def complete_gainers_losers():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={av_api}"
    requests = r.get(url)
    data_json = requests.json()
    return data_json

    
    
    
    
    
    
    
    
    
    
"""