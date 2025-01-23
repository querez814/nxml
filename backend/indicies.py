from fastapi import APIRouter
from finvizfinance.screener.overview import Overview
import requests as r 
import os
import dotenv as env
import pandas as pd

APIRouter()



def screener(exchange: str, sector:str):
    
    overview=Overview()
    filters_dict = {'Exchange':{exchange},'Sector': {sector}}

    overview.set_filter(filters_dict=filters_dict)
    df = overview.screener_view()
    df.head()

    return df

    
    