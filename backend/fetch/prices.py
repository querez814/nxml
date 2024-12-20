from fastapi import APIRouter, HTTPException
from fetch.income_statement import get_quarterly_statement_data
from fetch.cashflow import get_quarterly_cashflow_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
import requests as r
import dotenv as env
import os
import pandas as pd
env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/prices/{ticker}")
def get_prices(ticker: str):
    # Fetch data from Alpha Vantage API
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={av_api}"
    response = r.get(url)
    data_json = response.json()
    
    # Extract and transform the time series data
    time_series = data_json.get("Time Series (Daily)", {})
    transformed_data = []

    for date, values in time_series.items():
        # Flatten the data structure with "fiscalDateEnding" as the date key
        flattened_entry = {"fiscalDateEnding": date}
        for key, value in values.items():
            try:
                # Convert values to numeric format (float)
                flattened_entry[key] = round(float(value), 2)  # Ensure 2 decimal precision
            except ValueError:
                # Handle invalid numeric values
                flattened_entry[key] = 0  # Set invalid values to 0
        transformed_data.append(flattened_entry)

    # Convert to a Pandas DataFrame for additional cleaning
    prices_df = pd.DataFrame(transformed_data)

    # Return the cleaned and formatted data
    return prices_df.to_dict(orient="records")
