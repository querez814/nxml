
from fastapi import APIRouter, HTTPException
import yfinance as yf 
import requests as r
import pandas as pd
import dotenv as env
import os
import numpy as np
from packages import get_valuation

router = APIRouter()
env.load_dotenv()
polygon_api = os.getenv("POLYGON_API")




@router.get("/news/{ticker}")
async def specific_news(ticker: str):
    url = f"https://api.polygon.io/v2/reference/news?ticker=AMD&limit=10&apiKey={polygon_api}"  
    
    response =  r.get(url)
    response_json = response.json()
    news = response_json.get("results", [])
    news_df = pd.DataFrame(news)
    valuation_metrics = await get_valuation(ticker)
    val_df = pd.DataFrame(valuation_metrics)
    news_df["evtosales"] = val_df["evtosales"]
    news_df["evtogrossprofit"] = val_df["evtogrossprofit"]
    news_df["evtoebitda"] = val_df["evtoebitda"]
    news_df["evtonetincome"] = val_df["evtonetincome"]
    news_df["price_to_sales_ratio_ttm"] = val_df["price_to_sales_ratio_ttm"]
    final_response = news_df.to_dict(orient="records")
    return final_response


@router.get("/newnew")
def news_engine():
    market_result = yf.Search("stocks", 20, 20).news
    market_result_df = pd.DataFrame(market_result)
    selected_df = pd.DataFrame()
    selected_df["title"] = market_result_df["title"] 
    selected_df["publisher"] = market_result_df["publisher"]
    selected_df["providerPublishTime"] = market_result_df["providerPublishTime"]
    selected_df["relatedTickers"] = market_result_df["relatedTickers"]
    selected_df["url"] = market_result_df["thumbnail"]
    selected_df = selected_df.fillna('')
    final_json = selected_df.to_dict(orient="records")

    return final_json

    
@router.get("/cleaned") 
def cleaned_news():
   return  
