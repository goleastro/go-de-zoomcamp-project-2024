variable "credentials" {
  description = "My Credentials"
  default     = "./keys/go-de-zoomcamp-project-2024.json"
}

variable "project" {
  description = "Project"
  default     = "go-de-zoomcamp-project-2024"
}

variable "region" {
  description = "Region"
  default     = "EUROPE-WEST3"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "london_cycles"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "go-de-zoomcamp-project-2024-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Clases"
  default     = "STANDARD"
}