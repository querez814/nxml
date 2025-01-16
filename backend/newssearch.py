
from fastapi import APIRouter
import yfinance as yf 
import requests as r
import pandas as pd
import bs4
import nltk
import datetime

router = APIRouter()


@router.get("/newnew")
def news_engine():
    market_result = yf.Search("fed", 20, 20).news
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