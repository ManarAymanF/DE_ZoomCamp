import argparse
import subprocess
import pandas as pd
import pyarrow.parquet as pq
from time import time 
from sqlalchemy import create_engine


def convert_parquet_to_csv (parquet_file , csv_file):
    parquet_data = pd.read_parquet(parquet_file)
    parquet_data.to_csv(csv_file , index=False)

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    table_name=params.table_name
    url = params.url

    #download parquet file using wget
    subprocess.run(["wget" , args.url])

    #Assuming the download file is named output.parquet
    parquet_name = "yellow_tripdata_2023-01.parquet"
    csv_name="output.csv"

    convert_parquet_to_csv(parquet_name , csv_name)

    connection_url = f'postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.db}'

    # Create the SQLAlchemy engine
    engine = create_engine(connection_url)

    #engine= create_engine('postgresql://{user}:{password}@{host}:5432/{db}')

    data_iter = pd.read_csv(csv_name , iterator = True , chunksize= 100000)

    data = next(data_iter)

    data.tpep_pickup_datetime = pd.to_datetime(data.tpep_pickup_datetime)
    data.tpep_dropoff_datetime = pd.to_datetime(data.tpep_dropoff_datetime)


    data.head(n=0).to_sql(name = table_name , con=engine , if_exists = 'replace')

    data.to_sql(name = table_name , con=engine , if_exists = 'append')

    while True:
        t_start = time()
        data = next(data_iter)
        
        data.tpep_pickup_datetime = pd.to_datetime(data.tpep_pickup_datetime)
        data.tpep_dropoff_datetime = pd.to_datetime(data.tpep_dropoff_datetime)

        data.to_sql(name = table_name , con=engine , if_exists = 'append')

        t_end = time()
        print('inserted another chunk....., took %.3f second' % (t_end - t_start))    




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import data from a PostgreSQL database.")
    parser.add_argument("--user", help="PostgreSQL username")
    parser.add_argument("--password", help="PostgreSQL password")
    parser.add_argument("--host", help="PostgreSQL host")
    parser.add_argument("--port", type=int, help="PostgreSQL port")
    parser.add_argument("--db", help="PostgreSQL database name")
    parser.add_argument("--table_name", help="PostgreSQL table name")
    parser.add_argument("--url", help="URL for downloading Parquet file")

    args = parser.parse_args()
    main(args)