from fastapi import APIRouter, HTTPException
import requests as r
import dotenv as env
import os
import pandas as pd
import numpy as np
from fetch.prices import get_prices

env.load_dotenv()
av_api = os.getenv("ALPHA_VANTAGE")

router = APIRouter()

@router.get("/technical-analysis/{interval}/{ticker}")
def technical_analysis(interval: str, ticker: str):
    def interpret_macd(macd_data):
        interpreted_data = {}
        previous_values = None
        
        for date, values in macd_data.items():
            macd_line = float(values['MACD'])
            signal_line = float(values['MACD_Signal'])
            histogram = float(values['MACD_Hist'])
            
            analysis = {
                'values': {
                    'macd': macd_line,
                    'signal': signal_line,
                    'histogram': histogram
                },
                'signals': {
                    'trend': 'bullish' if macd_line > 0 else 'bearish',
                    'momentum': 'strengthening' if histogram > 0 else 'weakening',
                    'signal': 'buy' if macd_line > signal_line else 'sell',
                    'strength': 'strong' if abs(histogram) > 0.5 else 'moderate' if abs(histogram) > 0.2 else 'weak'
                }
            }
            
            if abs(histogram) < 0.1:
                analysis['signals']['crossover'] = 'potential bullish crossover' if macd_line > signal_line else 'potential bearish crossover'
            
            if previous_values:
                prev_macd = float(previous_values['MACD'])
                prev_hist = float(previous_values['MACD_Hist'])
                analysis['signals']['acceleration'] = 'increasing' if abs(histogram) > abs(prev_hist) else 'decreasing'
                
            previous_values = values
            interpreted_data[date] = analysis
        return interpreted_data

    def interpret_rsi(rsi_data):
        returned_data = {}
        for date, values in rsi_data.items():
            if isinstance(values, dict) and 'RSI' in values:
                numeric_rsi = float(values['RSI'])
                returned_data[date] = {
                    'value': numeric_rsi,
                    'status': 'overbought' if numeric_rsi > 70 else 'oversold' if numeric_rsi < 30 else 'neutral',
                    'trend': 'bullish' if numeric_rsi > 50 else 'bearish',
                    'strength': 'strong' if abs(numeric_rsi - 50) > 20 else 'moderate' if abs(numeric_rsi - 50) > 10 else 'weak'
                }
        return returned_data

    def interpret_aroon(aroon_data):
        interpreted_data = {}
        previous_values = None
        
        for date, values in aroon_data.items():
            aroon_up = float(values['Aroon Up'])
            aroon_down = float(values['Aroon Down'])
            aroon_oscillator = aroon_up - aroon_down
            
            analysis = {
                'values': {
                    'aroon_up': aroon_up,
                    'aroon_down': aroon_down,
                    'aroon_oscillator': aroon_oscillator
                },
                'signals': {
                    'trend': 'strong_bullish' if aroon_up > 70 and aroon_down < 30 else
                            'strong_bearish' if aroon_down > 70 and aroon_up < 30 else
                            'bullish' if aroon_up > aroon_down else 'bearish',
                    'strength': 'strong' if abs(aroon_oscillator) > 50 else
                               'moderate' if abs(aroon_oscillator) > 30 else 'weak',
                    'consolidation': 'yes' if aroon_up < 30 and aroon_down < 30 else 'no',
                    'signal': 'buy' if aroon_up > aroon_down and aroon_up > 50 else
                             'sell' if aroon_down > aroon_up and aroon_down > 50 else 'hold'
                }
            }
            
            if previous_values:
                prev_up = float(previous_values['Aroon Up'])
                prev_down = float(previous_values['Aroon Down'])
                
                analysis['signals']['momentum'] = 'increasing' if aroon_oscillator > (prev_up - prev_down) else 'decreasing'
                
                if aroon_up > prev_up and aroon_down < prev_down:
                    analysis['signals']['crossover'] = 'potential bullish crossover'
                elif aroon_down > prev_down and aroon_up < prev_up:
                    analysis['signals']['crossover'] = 'potential bearish crossover'
            
            previous_values = values
            interpreted_data[date] = analysis
        return interpreted_data

    def interpret_stoch(stoch_data):
        interpreted_data = {}
        previous_values = None
        
        for date, values in stoch_data.items():
            slowk = float(values['SlowK'])
            slowd = float(values['SlowD'])
            
            analysis = {
                'values': {
                    'k_line': slowk,
                    'd_line': slowd
                },
                'signals': {
                    'status': 'overbought' if slowk > 80 else 
                             'oversold' if slowk < 20 else 'neutral',
                    'trend': 'bullish' if slowk > slowd else 'bearish',
                    'strength': 'strong' if abs(slowk - 50) > 30 else 
                               'moderate' if abs(slowk - 50) > 15 else 'weak',
                    'signal': 'buy' if slowk > slowd and slowk < 80 else
                             'sell' if slowk < slowd and slowk > 20 else 'hold'
                }
            }
            
            if previous_values:
                prev_k = float(previous_values['SlowK'])
                prev_d = float(previous_values['SlowD'])
                
                analysis['signals']['momentum'] = 'increasing' if slowk > prev_k else 'decreasing'
                
                if slowk > slowd and prev_k < prev_d:
                    analysis['signals']['crossover'] = 'bullish crossover'
                elif slowk < slowd and prev_k > prev_d:
                    analysis['signals']['crossover'] = 'bearish crossover'
            
            previous_values = values
            interpreted_data[date] = analysis
        return interpreted_data

    def get_overall_trend(macd, rsi, aroon, stoch):
        bullish_signals = sum([
            1 if 'bullish' in macd['signals']['trend'] else 0,
            1 if 'bullish' in rsi['trend'] else 0,
            1 if 'bullish' in aroon['signals']['trend'] else 0,
            1 if 'bullish' in stoch['signals']['trend'] else 0
        ])
        return 'bullish' if bullish_signals >= 3 else 'bearish'

    def get_signal_strength(macd, rsi, aroon, stoch):
        strong_signals = sum([
            1 if macd['signals']['strength'] == 'strong' else 0,
            1 if rsi['strength'] == 'strong' else 0,
            1 if aroon['signals']['strength'] == 'strong' else 0,
            1 if stoch['signals']['strength'] == 'strong' else 0
        ])
        return 'strong' if strong_signals >= 3 else 'moderate' if strong_signals >= 2 else 'weak'

    def get_recommended_action(macd, rsi, aroon, stoch):
        buy_signals = sum([
            1 if macd['signals']['signal'] == 'buy' else 0,
            1 if rsi['status'] == 'oversold' else 0,
            1 if aroon['signals']['signal'] == 'buy' else 0,
            1 if stoch['signals']['signal'] == 'buy' else 0
        ])
        sell_signals = sum([
            1 if macd['signals']['signal'] == 'sell' else 0,
            1 if rsi['status'] == 'overbought' else 0,
            1 if aroon['signals']['signal'] == 'sell' else 0,
            1 if stoch['signals']['signal'] == 'sell' else 0
        ])
        return 'buy' if buy_signals >= 3 else 'sell' if sell_signals >= 3 else 'hold'

    try:
        macd_response = r.get(f"https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval={interval}&series_type=close&apikey={av_api}")
        rsi_response = r.get(f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval={interval}&time_period=14&series_type=close&apikey={av_api}")
        aroon_response = r.get(f"https://www.alphavantage.co/query?function=AROON&symbol={ticker}&interval={interval}&time_period=14&apikey={av_api}")
        stoch_response = r.get(f"https://www.alphavantage.co/query?function=STOCH&symbol={ticker}&interval={interval}&apikey={av_api}")

        for response in [macd_response, rsi_response, aroon_response, stoch_response]:
            if 'Error Message' in response.json():
                raise HTTPException(status_code=400, detail=f"Alpha Vantage API error: {response.json()['Error Message']}")
            if 'Note' in response.json():
                raise HTTPException(status_code=429, detail=f"Alpha Vantage API limit reached: {response.json()['Note']}")

        macd_data = macd_response.json().get("Technical Analysis: MACD", {})
        rsi_data = rsi_response.json().get("Technical Analysis: RSI", {})
        aroon_data = aroon_response.json().get("Technical Analysis: AROON", {})
        stoch_data = stoch_response.json().get("Technical Analysis: STOCH", {})

        if not all([macd_data, rsi_data, aroon_data, stoch_data]):
            raise HTTPException(status_code=404, detail="No technical analysis data available for this ticker")

        processed_macd = interpret_macd(macd_data)
        processed_rsi = interpret_rsi(rsi_data)
        processed_aroon = interpret_aroon(aroon_data)
        processed_stoch = interpret_stoch(stoch_data)

        all_dates = sorted(set(macd_data.keys()) & set(rsi_data.keys()) & 
                         set(aroon_data.keys()) & set(stoch_data.keys()),
                         reverse=True)

        if not all_dates:
            raise HTTPException(status_code=404, detail="No overlapping data points found across indicators")

        combined_analysis = {}
        
        for date in all_dates:
            combined_analysis[date] = {
                'indicators': {
                    'macd': processed_macd[date],
                    'rsi': processed_rsi[date],
                    'aroon': processed_aroon[date],
                    'stochastic': processed_stoch[date]
                },
                'summary': {
                    'overall_trend': get_overall_trend(processed_macd[date], processed_rsi[date],
                                                     processed_aroon[date], processed_stoch[date]),
                    'signal_strength': get_signal_strength(processed_macd[date], processed_rsi[date],
                                                         processed_aroon[date], processed_stoch[date]),
                    'recommended_action': get_recommended_action(processed_macd[date], processed_rsi[date],
                                                              processed_aroon[date], processed_stoch[date])
                }
            }

        return {
            'status': 'success',
            'data': {
                'ticker': ticker,
                'interval': interval,
                'last_updated': all_dates[0],
                'analysis': combined_analysis
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))