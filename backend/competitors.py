from fastapi import APIRouter
from packages import get_valuation
import requests as r
from bs4 import BeautifulSoup
from fetch.is_computations import get_yoy,get_qoq,get_margins
import pandas as pd

router = APIRouter()

@router.get("/competitors/{ticker}")
def get_rival_stocks_scrape(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/profile"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = r.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for {ticker}. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    competitors = []
    
    
    section = soup.find(lambda tag: tag.name == "span" and "Competitors" in tag.text)
    if section:
        parent = section.find_parent()
        competitor_links = parent.find_all('a', href=True)
        for link in competitor_links:
            href = link['href']
            if '/quote/' in href:
                parts = href.split('/')
                if len(parts) > 2:
                    candidate = parts[2].split('?')[0]
                    if candidate.upper() != ticker.upper() and candidate not in competitors:
                        competitors.append(candidate)
    else:
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/quote/' in href:
                parts = href.split('/')
                if len(parts) > 2:
                    candidate = parts[2].split('?')[0]
                    if candidate.upper() != ticker.upper() and candidate not in competitors:
                        competitors.append(candidate)
    shortened_competitors = competitors[0:5] 
    shortened_competitors_df = pd.DataFrame(shortened_competitors)
    

    return shortened_competitors_df

@router.get("/q/is/{ticker}") 
def related_tickers_is(ticker: str):
    rivals = get_rival_stocks_scrape(ticker)
    rivals_metrics = []
    for rival in rivals:
        yoy =get_yoy(rival)
        rivals_metrics.append(yoy)
        qoq = get_qoq(rival)
        rivals_metrics.append(qoq)
        margins = get_margins(rival)
        rivals_metrics.append(margins)
        
    return rivals_metrics.to_dict(orient="records")

    
    
print(related_tickers_is("AMD"))