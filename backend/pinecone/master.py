
import os
import sys
import logging
import numpy as np
from pinecone import Pinecone
from dotenv import load_dotenv

# Add the parent directory of 'fetch' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fetch.balancesheet import get_quarterly_balance_sheet_data 
from fetch.cashflow import get_quarterly_cashflow_statement_data
from fetch.income_statement import get_quarterly_statement_data
from fastapi.exceptions import HTTPException

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
        tickers = {vec["metadata"].get("symbol", None) for vec in response.get("matches", []) if "symbol" in vec["metadata"]}
        logging.info(f"Fetched {len(tickers)} tickers from namespace: {namespace}")
        return list(tickers)
    except Exception as e:
        logging.error(f"Error fetching tickers from namespace {namespace}: {e}")
        return []

def safe_float(value):
    """Safely convert value to float."""
    try:
        return float(value.strip('%')) / 100 if isinstance(value, str) and "%" in value else float(value)
    except (ValueError, TypeError):
        return 0.0

def convert_to_vector(data, ticker, statement_type):
    """Convert financial statement data into a structured vector format."""
    required_dimension = 1536
    vectors = []

    for entry in data:
        fiscal_date = entry.get("fiscalDateEnding", "unknown")

        fields = []

        if statement_type == "income-statement":
            fields = [
                safe_float(entry.get("totalRevenue", 0)),
                safe_float(entry.get("costOfRevenue", 0)),
                safe_float(entry.get("costofGoodsAndServicesSold", 0)),
                safe_float(entry.get("grossMargin", 0)),
                safe_float(entry.get("sellingGeneralAndAdministrative", 0)),
                safe_float(entry.get("researchAndDevelopment", 0)),
                safe_float(entry.get("operatingExpenses", 0)),
                safe_float(entry.get("ebitda", 0)),
                safe_float(entry.get("operatingIncome", 0)),
                safe_float(entry.get("netIncome", 0)),
                safe_float(entry.get("operatingMargin", 0)),
                safe_float(entry.get("ebitdaMargin", 0)),
                safe_float(entry.get("netMargin", 0))
            ]

        elif statement_type == "cashflow-statement":
            fields = [
                safe_float(entry.get("netIncome", 0)),
                safe_float(entry.get("operatingCashflow", 0)),
                safe_float(entry.get("capitalExpenditures", 0)),
                safe_float(entry.get("freeCashFlow", 0)),
                safe_float(entry.get("changeInOperatingLiabilities", 0)),
                safe_float(entry.get("changeInOperatingAssets", 0)),
                safe_float(entry.get("depreciationDepletionAndAmortization", 0)),
                safe_float(entry.get("changeInReceivables", 0)),
                safe_float(entry.get("changeInInventory", 0)),
                safe_float(entry.get("cashflowFromFinancing", 0)),
                safe_float(entry.get("net_profit_margin", 0)),
                safe_float(entry.get("ocf_margin", 0)),
                safe_float(entry.get("fcf_margin", 0)),
                safe_float(entry.get("roce", 0)),
            ]

        elif statement_type == "balancesheet-statement":
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
                safe_float(entry.get("current_ratio", 0)),
                safe_float(entry.get("quick_ratio", 0)),
                safe_float(entry.get("cash_ratio", 0)),
                safe_float(entry.get("debt_to_equity_ratio", 0)),
            ]

        sanitized_values = [0.0 if not np.isfinite(v) else float(v) for v in fields]
        padded_values = np.pad(sanitized_values, (0, required_dimension - len(sanitized_values)), constant_values=0.0)

        metadata = {key: entry.get(key, None) for key in entry.keys()}
        metadata.update({"ticker": ticker, "fiscalDateEnding": fiscal_date})

        vectors.append({
            "id": f"{ticker}-{fiscal_date}-{statement_type}",
            "values": padded_values.tolist(),
            "metadata": metadata,
        })

    return vectors

def upsert_financial_data(namespace, statement_type, batch_size=10):
    """Fetch and upsert financial data into a specific namespace in smaller batches to prevent memory overflow."""
    tickers = fetch_tickers_from_pinecone(namespace="industry:semiconductors")

    for i in range(0, len(tickers), batch_size):
        batch_tickers = tickers[i:i + batch_size]
        all_vectors = []

        for ticker in batch_tickers:
            logging.info(f"Processing {statement_type} data for ticker: {ticker}")

            try:
                if statement_type == "income-statement":
                    financial_data = get_quarterly_statement_data(ticker)
                elif statement_type == "cashflow-statement":
                    financial_data = get_quarterly_cashflow_statement_data(ticker)
                elif statement_type == "balancesheet-statement":
                    financial_data = get_quarterly_balance_sheet_data(ticker)

                if not financial_data:
                    logging.warning(f"No valid {statement_type} data for {ticker}. Skipping.")
                    continue

                vectors = convert_to_vector(financial_data, ticker, statement_type)
                all_vectors.extend(vectors)

            except HTTPException as e:
                logging.warning(f"Skipping {ticker} due to missing reports: {e.detail}")
                continue

            except MemoryError:
                logging.error(f"MemoryError: Skipping {ticker} due to large dataset.")
                continue

        # Split large batch if exceeding Pinecone's 4MB limit
        chunk_size = 500
        for j in range(0, len(all_vectors), chunk_size):
            try:
                index.upsert(vectors=all_vectors[j:j + chunk_size], namespace=statement_type)
                logging.info(f"Upserted {len(all_vectors[j:j + chunk_size])} vectors into namespace {statement_type}.")
            except Exception as e:
                logging.error(f"Error upserting vectors to namespace {statement_type}: {e}")

if __name__ == "__main__":
    for statement_type in ["income-statement", "cashflow-statement", "balancesheet-statement"]:
        logging.info(f"Starting upsert for {statement_type}")
        upsert_financial_data(namespace=statement_type, statement_type=statement_type)
