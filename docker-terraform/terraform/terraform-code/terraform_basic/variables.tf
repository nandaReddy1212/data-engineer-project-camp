
variable "project_id" {
  description = "Project"
  default     = "vertexai-489303"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "The location of the resources to create."
  default     = "US"
}


variable "bq_dataset_name" {
  description = "The name of the BigQuery dataset to create."
  type        = string
  default     = "ride_company_dataset"


}


variable "gcs_bucket_name" {
  description = "The name of the GCS bucket to create."
  type        = string
  default     = "ride_company_bucket"


}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"

}