# Infrastructure as Code with Terraform on GCP

This project demonstrates how to provision and manage Google Cloud Platform (GPC) resources using Terraform within a GitHub Codespaces environment.

## 🚀 Workflow Summary

### 1. Prerequisites & Authentication
*   **Service Account:** Created a dedicated Service Account in the GCP Console.
*   **IAM Roles:** Assigned the following permissions to the Service Account:
    *   `BigQuery Admin`
    *   `Storage Admin` (GCS)
    *   `Compute Admin`
*   **Security:** Generated a JSON Key for the service account.
*   **GitHub Integration:** Added the JSON key content as a GitHub Secret (e.g., `GCP_CREDS`) to allow the Codespace terminal to authenticate securely.

### 2. Configuration Files
*   `main.tf`: Defines the provider (Google) and the specific resources (BigQuery datasets, GCS buckets, etc.).
*   `variables.tf`: Managed reusable values like `project_id`, `region`, and `bucket_name` to keep the code DRY and flexible.

### 3. Terraform Execution Steps
The following commands were used to manage the lifecycle of the infrastructure:

1.  **Initialize:** 
    ```bash
    terraform init
    ```
    *Downloads the Google provider plugins and initializes the backend.*

2.  **Format:** 
    ```bash
    terraform fmt
    ```
    *Automatically rewrites configuration files to canonical format and style.*

3.  **Plan:** 
    ```bash
    terraform plan
    ```
    *Creates an execution plan, showing exactly what resources will be created or modified without making changes yet.*

4.  **Apply:** 
    ```bash
    terraform apply
    ```
    *Executes the actions proposed in the plan to create the infrastructure in GCP.*

5.  **Destroy:** 
    ```bash
    terraform destroy
    ```
    *Removes all resources managed by this Terraform project to avoid ongoing costs.*

---

## 🛠 Troubleshooting Notes
*   **Port Conflicts:** If running local services (like Postgres) alongside Docker in Codespaces, ensure host ports (e.g., 5432) are not already allocated by pre-installed system services.
