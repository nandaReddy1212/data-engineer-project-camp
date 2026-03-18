# Kestra Data Platform: GCP & AI-Ready Orchestration
This repository contains the orchestration logic for a modern data stack using Kestra, Docker, and Google Cloud Platform (GCP). It handles everything from historical batch ingestion to scheduled backfills, with a roadmap toward integrated AI workflows.
### Architecture
Orchestrator: Kestra (Self-hosted via Docker Compose)
Infrastructure: Google Cloud Platform (GCS & BigQuery)
Authentication: GCP Service Account (JSON Key)
Data Strategy: Historical Batch Load ➔ Scheduling ➔ Backfill ➔ AI Enrichment (Future)


# Setup & Installation
1. Configure GCP Authentication
Place your service-account.json in the root directory. In your docker-compose.yml, ensure the file is mapped to the Kestra container:
yaml
volumes:
  - ./gcp-service-account.json:/app/gcp-service-account.json


# **Pipeline Logic:**
Historical Batch Load To handle the initial data migration, use the Historical Load flow. This flow:
1) *Scans source directories/APIs.*
2) Uploads data to a specific GCS bucket.
3) Creates BigQuery tables and performs an initial WRITE_TRUNCATE load.
4) Scheduling & Backfills The production flows use Kestra’s Schedule Trigger.
**Backfill:** To rerun data for past dates, use the "Backfill" button in the Kestra UI. Select the date range, and Kestra will execute the flow for each period using the {{ trigger.date }} variable.
5) Incremental Loads: New data is appended to BigQuery daily using WRITE_APPEND to maintain history.