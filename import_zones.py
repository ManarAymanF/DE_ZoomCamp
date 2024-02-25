import argparse
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Assuming the download file is named zones.csv
    csv_name = "zones.csv"

    # Create the SQLAlchemy engine
    connection_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

    engine = create_engine(connection_url)

    # Download and read CSV file
    data = pd.read_csv(url)

    # Insert data into PostgreSQL table
    data.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import data from a PostgreSQL database.")
    parser.add_argument("--user", help="PostgreSQL username")
    parser.add_argument("--password", help="PostgreSQL password")
    parser.add_argument("--host", help="PostgreSQL host")
    parser.add_argument("--port", type=int, help="PostgreSQL port")
    parser.add_argument("--db", help="PostgreSQL database name")
    parser.add_argument("--table_name", help="PostgreSQL table name")
    parser.add_argument("--url", help="URL for downloading CSV file")

    args = parser.parse_args()
    main(args)
