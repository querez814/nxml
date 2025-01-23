from fastapi import APIRouter, HTTPException
import dotenv as env
import pandas as pd
import requests as r
import os
from datetime import datetime
from packages import get_valuation
from fetch.technicals import technical_analysis

env.load_dotenv()
news_api = os.getenv("STOCK_NEWS_API_KEY")
router = APIRouter()

@router.get("/general")
async def general_news():
    market_news_url = f"https://stocknewsapi.com/api/v1/category?section=general&items=8&page=1&token={os.getenv("STOCK_NEWS_API_KEY")}"
    response = r.get(market_news_url)
    #enforce json
    response_native = response.json()
    general_news_for_front_page = response_native["data"]
    
    return general_news_for_front_page




@router.get("/{ticker}")
async def get_ticker_news(ticker:str):
    news_url = f"https://stocknewsapi.com/api/v1?tickers={ticker}&items=50&page=1&token={os.getenv("STOCK_NEWS_API_KEY")}" 
    response = r.get(news_url)
    #enforce json
    response_native = response.json()
    response_data = response_native["data"]

    #get analyst upgrade/downgrade
    analyst_rate_url = f"https://stocknewsapi.com/api/v1/ratings?tickers={ticker}&items=10&page=1&token={os.getenv("STOCK_NEWS_API_KEY")}"
    analyst_rate_response = r.get(analyst_rate_url)
    #enforce json
    analyst_rate_native = analyst_rate_response.json()
    analyst_rate_data = analyst_rate_native["data"]
    
    #get valuation data
    val = await get_valuation(ticker)
    valuation_results =[]
    for metric in val:
        formatted_item = metric.copy()
        valuation_results.append(formatted_item)

    #Get technical data for the entrypoint algo    
    """
    technicals = await technical_analysis("daily", ticker)
    technicals_results = [] 
    for indicator in technicals:
        formatted_item = indicator.copy()
        technicals_results.append(formatted_item)
"""
        
        

    return  {
        "ticker": ticker,
        "news": response_data,
        "analystcoverage":analyst_rate_data,
        "valuation": valuation_results[0],
  #      "entry": technicals_results[0]
    } 