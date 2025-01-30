
from fastapi import APIRouter
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any, Tuple
import statistics
from datetime import datetime, timedelta
from fetch.prices import get_closing_prices
import json

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

@router.get("/dmi/{ticker}")
def get_dmi(ticker:str):
    url = f"https://www.alphavantage.co/query?function=DX&symbol={ticker}&interval=daily&time_period=50&apikey={av_api}"
    data = r.get(url).json()
    dmi = data["Technical Analysis: DX"]
    closing_prices = get_closing_prices(ticker)
    price_index = 0 
    dmi_items = sorted(list(dmi.items()), key=lambda x: x[0], reverse = True)
    dmi_points = []
    return dmi_items
    
    

    return