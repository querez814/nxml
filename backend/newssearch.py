from fastapi import APIRouter, HTTPException
import dotenv as env
import pandas as pd
import requests as r
import os
from datetime import datetime
from packages import get_valuation



env.load_dotenv()
router = APIRouter()
polygon_api = os.getenv("POLYGON_API_KEY")

def format_utc_timestamp(utc_str: str) -> str:
    """Convert UTC timestamp string to a readable format."""
    try:
        dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%A, %B %d, %Y at %I:%M %p UTC")
    except ValueError as e:
        return utc_str  # Return original string if parsing fails

@router.get("/news/{ticker}")
async def ticker_news(ticker: str):
    try:
        url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&limit=10&apiKey={polygon_api}"
        response = r.get(url)
        response.raise_for_status()  
        json_response = response.json()
        val = await get_valuation(ticker)
        
        formatted_results = []
        valuation_results = []

        for metric in val:
            formatted_item = metric.copy()
            valuation_results.append(formatted_item)

        for news_item in json_response["results"]:
            formatted_item = news_item.copy()
            formatted_item["published_utc"] = format_utc_timestamp(news_item["published_utc"])
            formatted_results.append(formatted_item)
        
        return {
            "ticker": ticker,
            "count": len(formatted_results),
            "news": formatted_results,
            "valuation": valuation_results[0]
        }
        
    except r.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching news from Polygon API: {str(e)}"
        )
    except KeyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected response format from Polygon API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
"""
@router.get("/news/{ticker}")
async def specific_news(ticker: str):
    url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&limit=10&apiKey={polygon_api}"  
    
    response =  r.get(url)
    response_json = response.json()
    news = response_json.get("results", [])
    news_df = pd.DataFrame(news)
    news_df["ticker"] = ticker
    valuation_metrics = await get_valuation(ticker)
    val_df = pd.DataFrame(valuation_metrics)
    news_df["evtosales"] = val_df["evtosales"]
    news_df["evtogrossprofit"] = val_df["evtogrossprofit"]
    news_df["evtoebitda"] = val_df["evtoebitda"]
    news_df["evtonetincome"] = val_df["evtonetincome"]
    news_df["price_to_sales_ratio_ttm"] = val_df["price_to_sales_ratio_ttm"]
    final_response = json.loads(news_df.to_json(orient="records"))
    return final_response
"""


"""
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
"""