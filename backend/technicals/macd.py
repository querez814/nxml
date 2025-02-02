
from fastapi import APIRouter
import os
import dotenv as env
import requests as r
env.load_dotenv
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/macdr/{ticker}")
def macd_1y(ticker:str, limit = 365):

    url = f"https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval=daily&series_type=close&apikey={av_api}"
    data = r.get(url).json()
    macd = data["Technical Analysis: MACD"]
    items = sorted(list(macd.items()), key=lambda x: x[0], reverse=True)
    return [{"date": date, "macd": float(vals["MACD"]), 
             "macd_signal": float(vals["MACD_Signal"]), 
             "macd_hist": float(vals["MACD_Hist"])} 
            for date, vals in items][:limit]