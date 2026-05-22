from fastapi import APIRouter, HTTPException
import asyncio
import dotenv as env
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import pytz
from collections import Counter

from fetch.av_util import av_get_json_sync
from fetch.news_sentiment import fetch_news_sentiment_async
from fetch.prices import get_daily_prices_compact_async

env.load_dotenv()

av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()


@router.get("/summary/{ticker}")
def get_summary(ticker:str):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={av_api}"
    return av_get_json_sync(url)


def get_individual_sentiment(ticker_sentiment: float) -> str:
    if ticker_sentiment >= 0.50:
        return "Strongly Bullish"
    elif ticker_sentiment >= 0.35:
        return "Moderately Bullish"
    
    elif ticker_sentiment < 0.35 or ticker_sentiment >= 0:
        return "Neutral"
    elif ticker_sentiment <= -0.35:
        return "Strongly Bearish"
    elif ticker_sentiment <= -0.15:
        return "Moderately Bearish"
    else:
        return "Neutral"

def extract_key_topics(articles: List[dict]) -> List[str]:
    all_topics = []
    for article in articles:
        for topic in article.get('topics', []):
            if isinstance(topic, dict):
                all_topics.append(topic.get('topic', ''))
            else:
                all_topics.append(topic)
    return [topic for topic, count in Counter(all_topics).most_common(5)]

def get_sentiment_trend(articles: List[dict]) -> str:
    if len(articles) < 2:
        return "Insufficient data"
        
    recent_sentiment = sum(a['overall_sentiment'] for a in articles[:5]) / min(5, len(articles))
    older_sentiment = sum(a['overall_sentiment'] for a in articles[-5:]) / min(5, len(articles[-5:]))
    
    diff = recent_sentiment - older_sentiment
    if diff > 0.1:
        return "Improving"
    elif diff < -0.1:
        return "Declining"
    return "Stable"

def extract_key_insights(article: Dict) -> List[str]:
    insights = []
    summary = article.get('summary', '').lower()
    
    if any(word in summary for word in ['leading', 'leader', 'dominant']):
        insights.append('Market Leadership')
    
    if any(word in summary for word in ['profit', 'revenue', 'earnings']):
        insights.append('Financial Performance')
    
    if any(word in summary for word in ['growth', 'expand', 'increase']):
        insights.append('Growth')
        
    if any(word in summary for word in ['ai', 'artificial intelligence', 'innovation']):
        insights.append('AI/Innovation')
        
    if any(word in summary for word in ['competitor', 'market share', 'versus']):
        insights.append('Competitive Analysis')
        
    return insights[:3]

def get_market_sentiment(articles: List[dict], distribution: Dict) -> Dict:
    if not articles:
        return {
            "overall": "Insufficient Data",
            "score": 0,
            "confidence": "Low"
        }
    
    total_weight = sum(a['ticker_relevance'] for a in articles[:5])
    if total_weight == 0:
        return {
            "overall": "Neutral",
            "score": 0,
            "confidence": "Low"
        }
    
    weighted_sentiment = sum(a['ticker_sentiment'] * a['ticker_relevance'] for a in articles[:5]) / total_weight
    
    total_articles = sum(distribution.values())
    if total_articles == 0:
        return {
            "overall": "Neutral",
            "score": 0,
            "confidence": "Low"
        }
    
    distribution_score = (distribution['positive'] - distribution['negative']) / total_articles
    
    final_score = (weighted_sentiment + distribution_score) / 2
    
    if final_score >= 0.5:
        sentiment = "Strongly Bullish"
    elif final_score >= 0.35:
        sentiment = "Moderately Bullish"
    elif final_score <= 0.35 or final_score >= 0:
        sentiment = "Neutral"
    elif final_score <= -0.35:
        sentiment = "Strongly Bearish"
    elif final_score <= -0.15:
        sentiment = "Moderately Bearish"
    else:
        sentiment = "Neutral"
    
    confidence = "High" if len(articles) >= 10 else "Medium" if len(articles) >= 5 else "Low"
    
    return {
        "overall": sentiment,
        "score": round(final_score, 3),
        "confidence": confidence
    }

def curate_news(data_json: Dict[str, Any], ticker: str, sort_by: str = 'relevance', min_relevance: float = 0.3, excluded_sources: List[str] = ['Motley Fool']) -> Dict[str, Any]:
    if not data_json or 'feed' not in data_json:
        return {"error": "No news data available"}

    articles = data_json['feed']
    curated_articles = []
    
    for article in articles:
        if article['source'] in excluded_sources:
            continue
            
        ticker_data = next((s for s in article.get('ticker_sentiment', []) 
                          if s['ticker'] == ticker), None)
        
        if not ticker_data or float(ticker_data['relevance_score']) < min_relevance:
            continue
            
        pub_time = datetime.strptime(article['time_published'], '%Y%m%dT%H%M%S')
        pub_time = pytz.utc.localize(pub_time).date()
        
        insights = extract_key_insights(article)
        ticker_sentiment = float(ticker_data['ticker_sentiment_score'])
        
        enriched_article = {
            'title': article['title'],
            'url': article['url'],
            'published_at': pub_time.isoformat(),
            'source': article['source'],
            'summary': article['summary'],
            'ticker_relevance': float(ticker_data['relevance_score']),
            'ticker_sentiment': ticker_sentiment,
            'sentiment_label': get_individual_sentiment(ticker_sentiment),
            'overall_sentiment': article.get('overall_sentiment_score', 0),
            'key_insights': insights,
            'topics': [t['topic'] for t in article.get('topics', []) 
                      if float(t['relevance_score']) > 0.5]
        }
        
        curated_articles.append(enriched_article)

    sort_keys = {
        'recent': lambda x: x['published_at'],
        'relevance': lambda x: x['ticker_relevance'],
        'sentiment': lambda x: abs(x['ticker_sentiment']),
        
    }
    curated_articles.sort(key=sort_keys.get(sort_by, sort_keys['relevance']), reverse=True)

    key_topics = extract_key_topics(articles)
    sentiment_trend = get_sentiment_trend(curated_articles)
    
    sentiment_buckets = {
        'positive': [a for a in curated_articles if a['ticker_sentiment'] > 0.15],
        'negative': [a for a in curated_articles if a['ticker_sentiment'] < -0.15],
        'neutral': [a for a in curated_articles if -0.15 <= a['ticker_sentiment'] <= 0.15]
    }

    sentiment_distribution = {
        'positive': len(sentiment_buckets['positive']),
        'neutral': len(sentiment_buckets['neutral']),
        'negative': len(sentiment_buckets['negative'])
    }

    market_sentiment = get_market_sentiment(curated_articles, sentiment_distribution)

    return {
        'ticker': ticker,
        'market_sentiment': market_sentiment,
        'summary': {
            'total_relevant_articles': len(curated_articles),
            'sentiment_trend': sentiment_trend,
            'key_topics': key_topics,
            'sentiment_distribution': sentiment_distribution,
            'market_sentiment': market_sentiment
        },
        'top_articles': curated_articles[:5],
        'sentiment_analysis': {
            'positive': sentiment_buckets['positive'][:3],
            'negative': sentiment_buckets['negative'][:3]
        },
        'market_context': {
            'trending_topics': key_topics,
            'sentiment_trend': sentiment_trend,
            'market_sentiment': market_sentiment
        }
    }


def _max_ticker_relevance(article: Dict[str, Any]) -> float:
    ts = article.get("ticker_sentiment") or []
    if not ts:
        return 0.0
    best = 0.0
    for x in ts:
        try:
            best = max(best, float(x.get("relevance_score", 0)))
        except (TypeError, ValueError):
            continue
    return best


def curate_market_news(
    data_json: Dict[str, Any],
    sort_by: str = "recent",
    min_ticker_relevance: float = 0.0,
    excluded_sources: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Curate AV news feed for broad market / landing: no single-ticker filter; uses overall sentiment."""
    if excluded_sources is None:
        excluded_sources = ["Motley Fool"]
    if not data_json or "feed" not in data_json:
        return {"error": "No news data available"}

    articles = data_json["feed"]
    curated_articles: List[Dict[str, Any]] = []

    for article in articles:
        if article.get("source") in excluded_sources:
            continue
        max_rel = _max_ticker_relevance(article)
        if max_rel < min_ticker_relevance:
            continue

        pub_time = datetime.strptime(article["time_published"], "%Y%m%dT%H%M%S")
        pub_time = pytz.utc.localize(pub_time).date()

        try:
            overall = float(article.get("overall_sentiment_score", 0) or 0)
        except (TypeError, ValueError):
            overall = 0.0

        insights = extract_key_insights(article)
        rel_weight = max(max_rel, 0.01)

        enriched_article = {
            "title": article["title"],
            "url": article["url"],
            "published_at": pub_time.isoformat(),
            "source": article["source"],
            "summary": article.get("summary", ""),
            "ticker_relevance": rel_weight,
            "ticker_sentiment": overall,
            "sentiment_label": get_individual_sentiment(overall),
            "overall_sentiment": overall,
            "key_insights": insights,
            "topics": [
                t["topic"]
                for t in article.get("topics", [])
                if isinstance(t, dict) and float(t.get("relevance_score", 0)) > 0.5
            ],
        }
        curated_articles.append(enriched_article)

    sort_keys = {
        "recent": lambda x: x["published_at"],
        "relevance": lambda x: x["ticker_relevance"],
        "sentiment": lambda x: abs(x["ticker_sentiment"]),
    }
    curated_articles.sort(
        key=sort_keys.get(sort_by, sort_keys["recent"]), reverse=True
    )

    key_topics = extract_key_topics(articles)
    sentiment_trend = get_sentiment_trend(curated_articles)

    sentiment_buckets = {
        "positive": [a for a in curated_articles if a["ticker_sentiment"] > 0.15],
        "negative": [a for a in curated_articles if a["ticker_sentiment"] < -0.15],
        "neutral": [
            a
            for a in curated_articles
            if -0.15 <= a["ticker_sentiment"] <= 0.15
        ],
    }

    sentiment_distribution = {
        "positive": len(sentiment_buckets["positive"]),
        "neutral": len(sentiment_buckets["neutral"]),
        "negative": len(sentiment_buckets["negative"]),
    }

    market_sentiment = get_market_sentiment(curated_articles, sentiment_distribution)

    return {
        "ticker": "MARKET",
        "market_sentiment": market_sentiment,
        "summary": {
            "total_relevant_articles": len(curated_articles),
            "sentiment_trend": sentiment_trend,
            "key_topics": key_topics,
            "sentiment_distribution": sentiment_distribution,
            "market_sentiment": market_sentiment,
        },
        "top_articles": curated_articles[:5],
        "sentiment_analysis": {
            "positive": sentiment_buckets["positive"][:3],
            "negative": sentiment_buckets["negative"][:3],
        },
        "market_context": {
            "trending_topics": key_topics,
            "sentiment_trend": sentiment_trend,
            "market_sentiment": market_sentiment,
        },
    }


async def _fetch_alpha_vantage_news_sentiment(ticker: str) -> Dict[str, Any]:
    return await fetch_news_sentiment_async(tickers=ticker, limit=50)


@router.get("/news/{ticker}")
async def get_curated_news(
    ticker: str, 
    sort_by: str = 'recent',
    min_relevance: float = 0.3,
    excluded_sources: str = 'Motley Fool'
):
    from fetch.valuations import get_valuation_async

    async def _valuation_safe():
        try:
            return await get_valuation_async(ticker)
        except Exception:
            return None

    async def _prices_safe():
        try:
            return await get_daily_prices_compact_async(ticker)
        except Exception:
            return []

    data_json, ttm_valuation, prices_list = await asyncio.gather(
        _fetch_alpha_vantage_news_sentiment(ticker),
        _valuation_safe(),
        _prices_safe(),
    )

    excluded_list = [s.strip() for s in excluded_sources.split(',')]
    curated_data = curate_news(data_json, ticker, sort_by, min_relevance, excluded_list)

    if ttm_valuation:
        latest = ttm_valuation[0]
        ttm_keys = [
            "pe_ratio", "pe_fwd", "pe_fwd_nongaap", "peg_ratio", "peg_nongaap_fwd",
            "ps_ttm", "ps_fwd", "pb_ratio",
            "price_to_cash_flow_ttm", "price_to_fcf_ttm",
            "ev_to_revenue", "ev_to_sales_fwd", "ev_to_ebitda", "ev_to_ebit",
            "ev_to_gross_profit", "ev_to_fcf_ttm", "ev_to_net_income",
            "dividend_yield", "dividend_yield_ttm", "payout_ratio",
            "roe_ttm", "roa_ttm", "profit_margin", "operating_margin_ttm",
            "book_value_per_share", "diluted_eps_ttm", "revenue_per_share_ttm",
            "beta", "week52_high", "week52_low", "ma_50d", "ma_200d",
            "analyst_target_price",
            "analyst_rating_strong_buy", "analyst_rating_buy", "analyst_rating_hold",
            "analyst_rating_sell", "analyst_rating_strong_sell",
            "sector", "industry",
        ]
        curated_data["ttm_display"] = {k: latest.get(k) for k in ttm_keys}

    if prices_list:
        prices_list.sort(key=lambda p: p["fiscalDateEnding"], reverse=True)
        latest_price_record = prices_list[0]
        curated_data["latest_price"] = {
            "date": latest_price_record["fiscalDateEnding"],
            "open": latest_price_record["1. open"],
            "high": latest_price_record["2. high"],
            "low": latest_price_record["3. low"],
            "close": latest_price_record["4. close"],
            "volume": latest_price_record["6. volume"],
        }
    else:
        curated_data["latest_price"] = {
            "error": "No price data available"
        }
    
    return curated_data
