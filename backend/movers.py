from fastapi import APIRouter
import dotenv as env
import os
import requests as r
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()

@router.get("/cgl")
def fetch_cgl():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={av_api}"
    data = r.get(url).json()
    return data
