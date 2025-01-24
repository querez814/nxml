from fastapi import APIRouter
import psycopg2
from nltk.sentiment import SentimentIntensityAnalyzer
from finvizfinance.screener.overview import Overview
from newssearch import general_news, get_ticker_news
import requests as r 
import os
import dotenv as env
import pandas as pd

router = APIRouter()

    
    
    