from fastapi import APIRouter
import os
import dotenv as env
import requests as r
env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")
router = APIRouter()



@router.get("/earningscalendar")
def get_earnings_calendar():
    url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={av_api}"
    response = r.get(url)
    #Enforce JSON
    response_json = response.json()

    return response_json 