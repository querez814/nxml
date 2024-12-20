from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/summary/{ticker}")
def get_summary(ticker:str):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()
    
    return data_json

    