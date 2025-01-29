from fastapi import APIRouter
import dotenv as env
import os
import requests as r
import pandas as pd

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

@router.get("/marketenv")
def get_mas():
    spy = "spy"
    qqq = "qqq"
    dia = "dia"

    spy_url_50_sma = f"https://www.alphavantage.co/query?function=SMA&symbol={spy}&interval=daily&time_period=50&series_type=open&apikey={av_api}"
    spy_50_response = r.get(spy_url_50_sma)
    spy_50_response_json = spy_50_response.json()

    spy_url_200_sma = f"https://www.alphavantage.co/query?function=SMA&symbol={spy}&interval=daily&time_period=200&series_type=open&apikey={av_api}"
    spy_200_response = r.get(spy_url_200_sma)
    spy_200_response_json = spy_200_response.json()

    qqq_url_50_sma = f"https://www.alphavantage.co/query?function=SMA&symbol={qqq}&interval=daily&time_period=50&series_type=open&apikey={av_api}"
    qqq_50_response = r.get(qqq_url_50_sma)
    qqq_50_response_json = qqq_50_response.json()

    qqq_url_200_sma = f"https://www.alphavantage.co/query?function=SMA&symbol={qqq}&interval=daily&time_period=200&series_type=open&apikey={av_api}"
    qqq_200_response = r.get(qqq_url_200_sma)
    qqq_200_response_json = qqq_200_response.json()

    dia_url_50_sma = f"https://www.alphavantage.co/query?function=SMA&symbol={dia}&interval=daily&time_period=50&series_type=open&apikey={av_api}"
    dia_50_response = r.get(dia_url_50_sma)
    dia_50_response_json = dia_50_response.json()

    dia_url_200_sma = f"https://www.alphavantage.co/query?function=SMA&symbol={dia}&interval=daily&time_period=200&series_type=open&apikey={av_api}"
    dia_200_response = r.get(dia_url_200_sma)
    dia_200_response_json = dia_200_response.json()
    
    return{
    }