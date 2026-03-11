import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option("--year", prompt="year", default=2021, type=int,
              help="year of the dataset")
@click.option("--month", prompt="month", default=1, type=int,
              help="month of the dataset")
@click.option("--pg-user", prompt="Postgres user", default="root")
@click.option("--pg-pass", prompt="Postgres password", default="root",
              hide_input=True)
@click.option("--pg-host", prompt="Postgres host", default="localhost")
@click.option("--pg-port", prompt="Postgres port", default=5432, type=int)
@click.option("--pg-database", prompt="Postgres database", default="ny_taxi")
@click.option("--chunksize", prompt="chunk size", default=10000, type=int)
@click.option("--target-table", prompt="table name", default="yellow_taxi_data")
def run(year, month,
        pg_user, pg_pass, pg_host, pg_port, pg_database,
        chunksize, target_table):
    """Download a single yellow taxi file and load it into Postgres."""
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = prefix + f'yellow_tripdata_{year:04d}-{month:02d}.csv.gz'
    engine = create_engine(
        f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_database}'
    )

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(n=0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )


if __name__ == '__main__':
    run()