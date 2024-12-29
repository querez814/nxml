
from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
from fastapi.responses import JSONResponse

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

crypto_router = APIRouter()

#HELPERS
def normalize_ticker(ticker:str) -> str:
    return ticker.upper() +"USD" if ticker.isalpha() else ticker.upper()



@crypto_router.get("/daily_quotes/{ticker}")
def get_daily_crypto_prices(ticker: str ):
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market=USD&apikey={av_api}"
    response = r.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Alpha Vantage API.")

    data_json = response.json()
    time_series = data_json.get("Time Series (Digital Currency Daily)", {})
    
    if not time_series:
        raise HTTPException(status_code=404, detail="No data found for the given ticker.")

    transformed_data = []

    for date, values in time_series.items():
        flattened_entry = {"date": date}
        for key, value in values.items():
            try:
                flattened_entry[key] = round(float(value), 2)
            except ValueError:
                flattened_entry[key] = 0
        transformed_data.append(flattened_entry)
    crypto_prices_df =pd.DataFrame(transformed_data)
    return crypto_prices_df.to_dict(orient="records") 
