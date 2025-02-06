import os
import time
import numpy as np
import logging
import psycopg2
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from fetch.income_statement import get_quarterly_statement_data
from fetch.balancesheet import get_quarterly_balance_sheet_data
from fetch.cashflow import get_quarterly_cashflow_statement_data
from fetch.valuations import get_valuation

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    filename="vector_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Pinecone Initialization
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define Pinecone Index
INDEX_NAME = "sec-filings-index"
VECTOR_DIMENSION = 1536  # Corrected dimension to match the Pinecone index

# Ensure the index exists
index_list = pc.list_indexes().names()
if INDEX_NAME not in index_list:
    pc.create_index(
        name=INDEX_NAME,
        dimension=VECTOR_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(INDEX_NAME)

def setup_db_url():
    """Modify the database URL to support Railway-specific configurations."""
    original_url = os.getenv("DATABASE_URL")
    if not original_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    if "postgres-production-0baf.up.railway.app" in original_url:
        return original_url.replace(
            "postgres-production-0baf.up.railway.app:5432",
            "monorail.proxy.rlwy.net:16462"
        )
    elif "postgres.railway.internal" in original_url:
        return original_url.replace(
            "postgres.railway.internal:5432",
            "monorail.proxy.rlwy.net:16462"
        )
    return original_url

def get_db_connection(database_url):
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            database_url,
            connect_timeout=60,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"Database connection error: {e}")
        raise

def fetch_ticker_list(database_url):
    """Fetch the list of tickers from the database."""
    conn = None
    cur = None
    try:
        conn = get_db_connection(database_url)
        cur = conn.cursor()
        cur.execute("SELECT symbol FROM stocks;")
        tickers = [row[0] for row in cur.fetchall()]
        print(f"[OK] Found {len(tickers)} tickers.")  # ASCII-compatible
        return tickers
    except Exception as e:
        logging.error(f"Error fetching ticker list: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def fetch_data(ticker):
    """Fetch financial data for a given ticker."""
    try:
        income_statement = get_quarterly_statement_data(ticker)
        balance_sheet = get_quarterly_balance_sheet_data(ticker)
        cash_flow = get_quarterly_cashflow_statement_data(ticker)
        valuation = get_valuation(ticker)
        return income_statement, balance_sheet, cash_flow, valuation
    except Exception as e:
        logging.warning(f"[WARN] Failed to fetch data for {ticker}: {e}")
        return None, None, None, None

def vectorize_features(income_statement, balance_sheet, cash_flow, valuation):
    """Convert financial data into a single vector."""
    try:
        # Flatten and concatenate all features
        return np.array([
            *(income_statement or [0.0] * (VECTOR_DIMENSION // 4)),
            *(balance_sheet or [0.0] * (VECTOR_DIMENSION // 4)),
            *(cash_flow or [0.0] * (VECTOR_DIMENSION // 4)),
            *(valuation or [0.0] * (VECTOR_DIMENSION // 4))
        ])
    except Exception as e:
        logging.error(f"Error vectorizing features: {e}")
        return None

def process_ticker(ticker):
    """Process a single ticker by fetching data, vectorizing it, and uploading it to Pinecone."""
    print(f"[...] Processing ticker: {ticker}")
    income_statement, balance_sheet, cash_flow, valuation = fetch_data(ticker)

    if not all([income_statement, balance_sheet, cash_flow, valuation]):
        logging.warning(f"Skipping {ticker} due to incomplete data.")
        return None

    vector = vectorize_features(income_statement, balance_sheet, cash_flow, valuation)
    
    if vector is None or len(vector) != VECTOR_DIMENSION:
        logging.error(f"Vector dimension mismatch for {ticker}. Expected {VECTOR_DIMENSION}, got {len(vector) if vector is not None else 'None'}.")
        return None

    try:
        index.upsert([(ticker, vector.tolist())])
        print(f"[OK] Processed {ticker} successfully.")
        return ticker
    except Exception as e:
        logging.error(f"Error uploading vector for {ticker}: {e}")
        return None

def main():
    """Main function to process all tickers."""
    database_url = setup_db_url()
    tickers = fetch_ticker_list(database_url)

    failed_tickers = []

    for ticker in tickers:
        result = process_ticker(ticker)
        if result is None:
            failed_tickers.append(ticker)

    if failed_tickers:
        logging.warning(f"Failed tickers: {failed_tickers}")
        with open("failed_tickers.txt", "w") as f:
            f.write("\n".join(failed_tickers))

    print("[DONE] Processing complete!")

if __name__ == "__main__":
    main()
