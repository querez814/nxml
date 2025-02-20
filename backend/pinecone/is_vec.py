
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
            vector=[0] * 1536,  # Dummy vector to fetch all metadata
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

def fetch_financial_data(symbol, statement_type="income-statement", max_retries=3, retry_delay=5):
    """Fetch latest financial statement data for a given ticker with retries."""
    url = f"{FINANCIAL_API_BASE}/{statement_type}/quarterly/{symbol}"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and data:
                return data[:4]  # Keep last 4 quarters
            logging.warning(f"No valid financial data found for {symbol}. Response: {data}")
            return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1}/{max_retries}: Error fetching financial data for {symbol}: {e}")
            time.sleep(retry_delay)
    logging.warning(f"Failed to fetch financial data for {symbol} after {max_retries} attempts. Skipping.")
    return []

def convert_to_vector(data, ticker):
    """Convert financial statement data into a structured vector format."""
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
            safe_float(entry.get("grossProfit", 0)),
            safe_float(entry.get("totalRevenue", 0)),
            safe_float(entry.get("costOfRevenue", 0)),
            safe_float(entry.get("operatingIncome", 0)),
            safe_float(entry.get("sellingGeneralAndAdministrative", 0)),
            safe_float(entry.get("researchAndDevelopment", 0)),
            safe_float(entry.get("operatingExpenses", 0)),
            safe_float(entry.get("incomeBeforeTax", 0)),
            safe_float(entry.get("incomeTaxExpense", 0)),
            safe_float(entry.get("ebit", 0)),
            safe_float(entry.get("ebitda", 0)),
            safe_float(entry.get("netIncome", 0)),
            safe_float(entry.get("grossMargin", 0)),
            safe_float(entry.get("operatingMargin", 0)),
            safe_float(entry.get("ebitMargin", 0)),
            safe_float(entry.get("ebitdaMargin", 0)),
            safe_float(entry.get("netMargin", 0))
        ]
        change_metrics = [
            "grossProfit_YoY", "grossProfit_QoQ", "totalRevenue_YoY", "totalRevenue_QoQ",
            "costOfRevenue_YoY", "costOfRevenue_QoQ", "operatingIncome_YoY", "operatingIncome_QoQ",
            "sellingGeneralAndAdministrative_YoY", "sellingGeneralAndAdministrative_QoQ",
            "researchAndDevelopment_YoY", "researchAndDevelopment_QoQ", "operatingExpenses_YoY",
            "operatingExpenses_QoQ", "incomeBeforeTax_YoY", "incomeBeforeTax_QoQ",
            "incomeTaxExpense_YoY", "incomeTaxExpense_QoQ", "ebit_YoY", "ebit_QoQ",
            "ebitda_YoY", "ebitda_QoQ", "netIncome_YoY", "netIncome_QoQ",
            "reportedEPS_YoY", "reportedEPS_QoQ", "estimatedEPS_YoY", "estimatedEPS_QoQ",
            "grossMargin_YoY", "grossMargin_QoQ", "operatingMargin_YoY", "operatingMargin_QoQ",
            "ebitMargin_YoY", "ebitMargin_QoQ", "ebitdaMargin_YoY", "ebitdaMargin_QoQ",
            "netMargin_YoY", "netMargin_QoQ"
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
    """Fetch tickers from Pinecone, retrieve financial data, and batch process vectors into Pinecone."""
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
