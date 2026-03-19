import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time
import logging

logging.basicConfig(level=logging.INFO)

BUCKET_NAME = 'cohorts-data-warehouse'

CREDENTIALS_FILE = "/workspaces/data-engineer-project-camp/workflow-orchestration/key.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"

MONTHS = [f"{i:02d}" for i in range(1, 7)]  # January to June
DOWNLOAD_DIR = "."

CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)

def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    local_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    if os.path.exists(local_path):
        logging.info(f"File {local_path} already exists. Skipping download.")
        return

    try:
        urllib.request.urlretrieve(url, local_path)
        logging.info(f"Downloaded {url} to {local_path}")
        return local_path
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return None
    
def create_bucket(bucket_name):
    try:
        # Get Bucket Details
        bucket = client.get_bucket(BUCKET_NAME)

        # check if the bucket belongs to the current project
        current_bucket_project_id = [bukt.id for bukt in client.list_buckets() if bukt.name == BUCKET_NAME][0]
        if bucket_name in current_bucket_project_id:
            logging.info(f"Bucket {bucket_name} belongs to the current project.")
        else:
            logging.warning(f"Bucket {bucket_name} does not belong to the current project.")
            sys.exit(1)
    except NotFound:
        logging.info(f"Bucket {bucket_name} not found. Creating bucket.")
        bucket = client.bucket(bucket_name)
        bucket.create(location="us-central1")
        logging.info(f"Bucket {bucket_name} created successfully.")
    except Forbidden:
        logging.error(f"Access denied to bucket {bucket_name}. Please check your permissions.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred while accessing or creating bucket {bucket_name}: {e}")
        sys.exit(1)

def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_file_to_gcs(local_path, max_retries=3):
    blob_name = os.path.basename(local_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    create_bucket(BUCKET_NAME)

    for attempt in range(max_retries):
        try:
            blob.upload_from_filename(local_path)
            logging.info(f"Uploaded {local_path} to GCS as {blob_name}")
            if verify_gcs_upload(blob_name):
                logging.info(f"Verified upload of {blob_name} to GCS.")
                return True
            else:
                logging.warning(f"Verification failed for {blob_name}. Retrying...")
        except Exception as e:
            logging.error(f"Error uploading {local_path} to GCS: {e}")
        
        time.sleep(2 ** attempt)  # Exponential backoff
    logging.error(f"Failed to upload {local_path} to GCS after {max_retries} attempts.")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    with ThreadPoolExecutor(max_workers=4) as executor:
        local_paths = list(executor.map(download_file, MONTHS))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_file_to_gcs, filter(None, local_paths))
    

        
