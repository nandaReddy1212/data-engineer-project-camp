       USER / BROWSER
             │
             ▼
      ┌───────────────┐      ┌────────────────────────────────┐
      │   pgAdmin     │◄────►│        INTERNAL NETWORK        │
      │ (Port: 8085)  │      │          (pg-network)          │
      └───────────────┘      └───────────────┬────────────────┘
                                             │
             ┌───────────────────────────────┼───────────────────────────────┐
             │                               │                               │
             ▼                               ▼                               ▼
    ┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
    │  DATA LOADER    │             │   POSTGRES DB   │             │  DOCKER VOLUME  │
    │ (Python + UV)   │────────────►│  (Service Name: │────────────►│ (Named: ny_taxi_│
    │ Run: zones.py   │   (SQL)     │   pgdatabase)   │  (Storage)  │  postgres_data) │
    └─────────────────┘             └─────────────────┘             └─────────────────┘
             ▲                               ▲
             │                               │
      ┌──────┴──────┐                 ┌──────┴──────┐
      │ SOURCE DATA │                 │ USER CONFIG │
      │ (CSV/URLs)  │                 │ (.env/YAML) │
      └─────────────┘                 └─────────────┘


Data Loader: You trigger this via docker compose run. It pulls data from the source and sends it to the Postgres DB.
Internal Network: The services talk to each other using names (like pgdatabase) instead of IP addresses.
Postgres DB: Receives the data and stores it permanently in the Docker Volume.
pgAdmin: You connect to this through your browser to see the tables inside the database.

# Move to the pipeline directory
cd pipeline

# Start Postgres and pgAdmin in the background
docker compose up -d

# Perform a clean build to ensure all files and dependencies are included
docker compose build --no-cache data-loader


# Verifiy internal files
docker compose run --rm --entrypoint /bin/sh data-loader -c "ls /code"

# Free up disk space: 
docker system prune -f


# running the pipeline for dynamic ingestion

1) docker compose run --rm data-loader zones.py [FLAGS]: Runs the specific script for the Zones table using the pre-built image environment.

2) docker compose run --rm data-loader ingest_data.py [FLAGS]: Runs the Yellow Taxi script, allowing you to pass dynamic arguments like --year and --month.

# why using rm in the script
--rm: This flag ensures the "one-off" container is automatically deleted after the script finishes, keeping your environment tidy.
