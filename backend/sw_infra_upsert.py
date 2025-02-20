
import os
import dotenv as env
import psycopg2
from pinecone import Pinecone, ServerlessSpec
import openai
import logging
env.load_dotenv()
# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# Initialize OpenAI
openai.api_key = OPEN_AI_API_KEY

# Initialize Pinecone
pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index('fundybot')  # Use the existing index

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_software_infrastructure_stocks():
    """Fetch tickers and company names for 'Software - Infrastructure' stocks."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = """
            SELECT symbol, company_name
            FROM stocks
            WHERE industry = 'Software - Infrastructure';
        """
        cursor.execute(query)
        results = cursor.fetchall()

        stocks = [{"symbol": row[0], "company_name": row[1]} for row in results]
        logging.info(f"Fetched {len(stocks)} stocks for 'Software - Infrastructure'.")
        return stocks

    except Exception as e:
        logging.error(f"Error fetching data from PostgreSQL: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()


def generate_embedding(text):
    """Generate embedding for a given text using OpenAI."""
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=[text]
        )
        return response['data'][0]['embedding']
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        return [0.01] * 1536  # Return a dummy embedding if API fails


def upsert_to_pinecone(stocks):
    """Upserts stock data to Pinecone."""
    vectors = []
    namespace = "industry:software-infrastructure"  # Modular namespace for this industry

    for stock in stocks:
        symbol = stock["symbol"]
        company_name = stock["company_name"]

        # Generate embedding for the company name
        embedding = generate_embedding(f"{company_name} ({symbol})")

        vectors.append({
            "id": f"stock:{symbol}",
            "values": embedding,
            "metadata": {
                "symbol": symbol,
                "company_name": company_name,
                "industry": "Software - Infrastructure"
            }
        })

    # Upsert vectors to Pinecone
    try:
        index.upsert(vectors=vectors, namespace=namespace)
        logging.info(f"Upserted {len(vectors)} stocks to Pinecone in '{namespace}' namespace.")
    except Exception as e:
        logging.error(f"Error upserting data to Pinecone: {e}")


if __name__ == "__main__":
    # Step 1: Fetch data from PostgreSQL
    software_infrastructure_stocks = fetch_software_infrastructure_stocks()

    # Step 2: Upsert data to Pinecone
    if software_infrastructure_stocks:
        upsert_to_pinecone(software_infrastructure_stocks)
    else:
        logging.warning("No stocks fetched. Nothing to upsert to Pinecone.")
