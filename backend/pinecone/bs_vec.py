
import os
import requests
import logging
import time
import numpy as np
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "fundybot"

if INDEX_NAME not in pc.list_indexes().names():
    raise ValueError(f"Error: Pinecone index '{INDEX_NAME}' not found!")

index = pc.Index(INDEX_NAME)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API Base URL
FINANCIAL_API_BASE = "https://investorterminal-production.up.railway.app/financials"

def fetch_tickers_from_pinecone(namespace="industry:semiconductors"):
    """Fetch tickers stored in the Pinecone namespace."""
    try:
        logging.info(f"Fetching all tickers from Pinecone namespace: {namespace}")
        response = index.query(
            vector=[0] * 1536,
            top_k=10000,
            namespace=namespace,
            include_metadata=True
        )
        tickers = {vec["metadata"]["symbol"] for vec in response.get("matches", []) if "symbol" in vec["metadata"]}
        logging.info(f"Fetched {len(tickers)} tickers from namespace: {namespace}")
        return list(tickers)
    except Exception as e:
        logging.error(f"Error fetching tickers from namespace {namespace}: {e}")
        return []

def fetch_financial_data(symbol, statement_type="balancesheet-statement", max_retries=3, retry_delay=5):
    """Fetch latest balance sheet statement data for a given ticker with retries."""
    url = f"{FINANCIAL_API_BASE}/{statement_type}/quarterly/{symbol}"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and data:
                return data[:4]
            logging.warning(f"No valid financial data found for {symbol}. Response: {data}")
            return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1}/{max_retries}: Error fetching financial data for {symbol}: {e}")
            time.sleep(retry_delay)
    logging.warning(f"Failed to fetch financial data for {symbol} after {max_retries} attempts. Skipping.")
    return []

def convert_to_vector(data, ticker):
    """Convert balance sheet statement data into a structured vector format."""
    required_dimension = 1536
    vectors = []
    def safe_float(value):
        try:
            return float(value.strip('%')) / 100 if isinstance(value, str) and "%" in value else float(value)
        except (ValueError, TypeError):
            return 0.0
    for entry in data:
        fiscal_date = entry.get("fiscalDateEnding", "unknown")
        fields = [
            safe_float(entry.get("totalCurrentAssets", 0)),
            safe_float(entry.get("totalAssets", 0)),
            safe_float(entry.get("totalCurrentLiabilities", 0)),
            safe_float(entry.get("totalLiabilities", 0)),
            safe_float(entry.get("working_capital", 0)),
            safe_float(entry.get("totalShareholderEquity", 0)),
            safe_float(entry.get("commonStockSharesOutstanding", 0)),
            safe_float(entry.get("cashAndCashEquivalentsAtCarryingValue", 0)),
            safe_float(entry.get("inventory", 0)),
            safe_float(entry.get("propertyPlantEquipment", 0)),
            safe_float(entry.get("deferredRevenue", 0)),
            safe_float(entry.get("currentDebt", 0)),
            safe_float(entry.get("current_ratio", 0)),
            safe_float(entry.get("quick_ratio", 0)),
            safe_float(entry.get("cash_ratio", 0)),
            safe_float(entry.get("debt_to_equity_ratio", 0)),
            safe_float(entry.get("debt_to_asset_ratio", 0)),
            safe_float(entry.get("book_value_per_share", 0))
        ]
        change_metrics = [
            "totalCurrentAssets_YoY", "totalCurrentAssets_QoQ", "totalAssets_YoY", "totalAssets_QoQ",
            "totalCurrentLiabilities_YoY", "totalCurrentLiabilities_QoQ", "totalLiabilities_YoY", "totalLiabilities_QoQ",
            "working_capital_YoY", "working_capital_QoQ", "totalShareholderEquity_YoY", "totalShareholderEquity_QoQ",
            "commonStockSharesOutstanding_YoY", "commonStockSharesOutstanding_QoQ", "cashAndCashEquivalentsAtCarryingValue_YoY", "cashAndCashEquivalentsAtCarryingValue_QoQ",
            "inventory_YoY", "inventory_QoQ", "propertyPlantEquipment_YoY", "propertyPlantEquipment_QoQ",
            "current_ratio_YoY", "current_ratio_QoQ", "quick_ratio_YoY", "quick_ratio_QoQ",
            "cash_ratio_YoY", "cash_ratio_QoQ", "debt_to_equity_ratio_YoY", "debt_to_equity_ratio_QoQ",
            "debt_to_asset_ratio_YoY", "debt_to_asset_ratio_QoQ", "book_value_per_share_YoY", "book_value_per_share_QoQ"
        ]
        for metric in change_metrics:
            fields.append(safe_float(entry.get(metric, "0%")))
        sanitized_values = [0.0 if not np.isfinite(v) else float(v) for v in fields]
        padded_values = np.pad(sanitized_values, (0, required_dimension - len(sanitized_values)), constant_values=0.0)
        metadata = {key: entry.get(key, None) for key in entry.keys()}
        metadata.update({"ticker": ticker, "fiscalDateEnding": fiscal_date})
        vectors.append({
            "id": f"{ticker}-{fiscal_date}",
            "values": padded_values.tolist(),
            "metadata": metadata,
        })
    return vectors

def upsert_financial_data(namespace, batch_size=50):
    tickers = fetch_tickers_from_pinecone(namespace)
    for i in range(0, len(tickers), batch_size):
        batch_tickers = tickers[i:i + batch_size]
        all_vectors = []
        for ticker in batch_tickers:
            logging.info(f"Processing financial data for ticker: {ticker}")
            financial_data = fetch_financial_data(ticker)
            if not financial_data:
                logging.warning(f"No valid financial data available for {ticker}. Skipping.")
                continue
            vectors = convert_to_vector(financial_data, ticker)
            all_vectors.extend(vectors)
        if all_vectors:
            try:
                index.upsert(vectors=all_vectors, namespace=namespace)
                logging.info(f"Upserted {len(all_vectors)} vectors into namespace {namespace}.")
            except Exception as e:
                logging.error(f"Error upserting vectors to namespace {namespace}: {e}")

if __name__ == "__main__":
    namespace = "industry:semiconductors"
    upsert_financial_data(namespace)
