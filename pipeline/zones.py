import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click



@click.command()
@click.option("--pg-user", prompt="Postgres user", default="root")
@click.option("--pg-pass", prompt="Postgres password", default="root")
@click.option("--pg-host", prompt="Postgres host", default="localhost")
@click.option("--pg-port", prompt="Postgres port", default=5432, type=int)
@click.option("--pg-database", prompt="Postgres database", default="ny_taxi")
@click.option("--chunksize", prompt="chunk size", default=100, type=int)
@click.option("--target-table", prompt="table name", default="zones")
def run(pg_user, pg_pass, pg_host, pg_port, pg_database, chunksize, target_table):
    engine = create_engine(
        f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_database}'
    )
    
    df_zones_iter = pd.read_csv(
        #'pipeline/taxi_zone_lookup.csv',
        f'taxi_zone_lookup.csv',
        iterator=True,
        chunksize=chunksize
    )

    first = True
    for record in tqdm(df_zones_iter):
        if first:
            record.head(n=0).to_sql(name=target_table, con=engine, if_exists='replace')
            first = False
            
        record.to_sql(name=target_table, con=engine, if_exists='append')


if __name__ == '__main__':
    run()