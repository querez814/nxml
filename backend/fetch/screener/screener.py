import psycopg2
import pandas as pd
import os
import time
import sys
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_database_url():
    load_dotenv()
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

def get_db_connection(database_url, max_retries=3, retry_delay=5):
    last_exception = None
    for attempt in range(max_retries):
        try:
            print(f"Connection attempt {attempt + 1} of {max_retries}...")
            conn = psycopg2.connect(
                database_url,
                connect_timeout=60,
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=5
            )
            print("Connection successful!")
            return conn
        except psycopg2.OperationalError as e:
            last_exception = e
            if attempt < max_retries - 1:
                print(f"Connection failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("All connection attempts failed.")
                print(f"Last error: {str(e)}")
    
    if last_exception:
        raise last_exception

def create_stocks_table(database_url):
    conn = None
    cur = None
    
    create_table_query = """
    DROP TABLE IF EXISTS stocks;
    CREATE TABLE stocks (
        symbol VARCHAR(10),
        company_name VARCHAR(255),
        market_cap BIGINT,
        stock_price DECIMAL(10,2),
        percent_change VARCHAR(10),
        industry VARCHAR(255),
        volume BIGINT,
        pe_ratio DECIMAL(10,2),
        ent_value DECIMAL(15,2),
        mc_group VARCHAR(50),
        sector VARCHAR(255),
        change_1w VARCHAR(10),
        change_1m VARCHAR(10),
        change_6m VARCHAR(10),
        change_3m VARCHAR(10),
        change_ytd VARCHAR(10),
        change_1y VARCHAR(10),
        change_5y VARCHAR(10),
        source_file VARCHAR(255),
        loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        conn = get_db_connection(database_url)
        if not conn:
            raise ConnectionError("Failed to establish database connection")
            
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(create_table_query)
        print("Table created successfully")
        
    except Exception as e:
        print(f"Error creating table: {e}")
        raise
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"\nColumns in CSV: {df.columns.tolist()}")
        
        df.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df.columns]
        df = df.rename(columns={
            '%_change': 'percent_change',
            'ent__value': 'ent_value'  
        })
        print(f"Cleaned columns: {df.columns.tolist()}")
        
        print("\nFirst row of data:")
        print(df.iloc[0].to_dict())
        
        percent_columns = ['percent_change', 'change_1w', 'change_1m', 'change_6m', 
                         'change_3m', 'change_ytd', 'change_1y', 'change_5y']
        for col in percent_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('%', '')
        
        df['source_file'] = os.path.basename(file_path)
        
        return df
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def load_to_database(df, database_url):
    """Load DataFrame to database."""
    if df is None or df.empty:
        print("No data to load")
        return
    
    conn = None
    cur = None
    
    try:
        conn = get_db_connection(database_url)
        if not conn:
            raise ConnectionError("Failed to establish database connection")
            
        cur = conn.cursor()
        
        records = df.to_dict('records')
        columns = df.columns.tolist()
        
        print("\nColumns being inserted:", columns)
        print("Number of columns:", len(columns))
        if records:
            print("First record length:", len(records[0]))
            print("First record data:", [records[0][col] for col in columns])
        
        insert_query = sql.SQL("INSERT INTO stocks ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        
        print("\nInsert query:", insert_query.as_string(conn))
        
        values = [[record[column] for column in columns] for record in records]
        
        cur.executemany(insert_query.as_string(conn), values)
        conn.commit()
        
        print(f"Successfully loaded {len(records)} records")
        
    except Exception as e:
        print(f"Error loading data to database: {e}")
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    try:
        database_url = setup_database_url()
        print("Testing database connection...")
        print(f"Using database URL: {database_url.split('@')[0]}@[HIDDEN]")
        
        create_stocks_table(database_url)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_dir = script_dir
        print(f"Looking for CSV files in: {csv_dir}")
        
        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
        if not csv_files:
            print("No CSV files found in directory")
            return
            
        print(f"\nFound {len(csv_files)} CSV files to process")
        for csv_file in csv_files:
            print(f"- {csv_file}")
        
        print("\nStarting processing...")
        for csv_file in csv_files:
            print(f"\nProcessing {csv_file}...")
            try:
                file_path = os.path.join(csv_dir, csv_file)
                df = process_csv(file_path)
                if df is not None:
                    print(f"Successfully read {csv_file}, attempting database load...")
                    load_to_database(df, database_url)
                else:
                    print(f"Failed to process {csv_file}")
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
                print("Full error:", sys.exc_info())
                continue
    
    except Exception as e:
        print(f"Critical error in main execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()