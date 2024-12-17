# Categories Web Scraper & Taxonomy Generator

A Flask-based web application that uses Playwright for web scraping and Google Cloud Vertex AI for generating hierarchical taxonomies.

## Local Development

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Docker (optional, for containerized development)
- Google Cloud project with Vertex AI API enabled
- Google Cloud credentials configured

### Setup Local Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Set required environment variables:
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Deployment to Google Cloud Run

### Prerequisites
- Google Cloud SDK
- Terraform
- Service account with required permissions:
  - Cloud Run Admin
  - Service Account User
  - Storage Admin
  - Vertex AI User

### Deployment Steps

1. Configure your Google Cloud project and set required environment variables:
```bash
# Login and set project
gcloud auth login
gcloud config set project ${GOOGLE_CLOUD_PROJECT}

# Set deployment environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"
export REGION="us-central1"  # or your preferred region
```

2. Update the variables in `terraform/terraform.tfvars`:
```hcl
project_id = "your-project-id"
region     = "us-central1"
service_name = "categories-app"
```

3. Initialize Terraform and set up base infrastructure:
```bash
cd terraform
terraform init
# Apply the infrastructure components (APIs and Cloud Build permissions)
terraform apply -target=google_project_service.container_registry \
               -target=google_project_service.cloud_build \
               -target=google_project_iam_member.cloud_build_storage \
               -target=google_project_iam_member.cloud_build_service_account
```

4. Build and push your application container image:
```bash
cd ..  # back to project root
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/categories-app:latest
```

5. Deploy the Cloud Run service:
```bash
cd terraform
terraform apply
```

The application will be available at the URL provided in the Terraform output.

### Infrastructure Details

The application is deployed with the following configuration:
- 10-minute timeout for long-running operations
- 2 CPU and 2GB memory allocation (required for Vertex AI processing)
- Public access enabled
- Automatic scaling based on demand
- Service account with Vertex AI access
- Docker images stored in Google Container Registry (GCR)
- Cloud Build service account with permissions:
  - Storage Admin (for pushing to GCR)
  - Cloud Build Builder

### Terraform Structure

The terraform configuration is split into multiple files to handle dependencies properly:
- `main.tf` - Provider configuration
- `infrastructure.tf` - API enablement and Cloud Build permissions
- `service.tf` - Cloud Run service deployment
- `variables.tf` - Variable definitions
- `terraform.tfvars` - Variable values

## Project Structure

```
.
├── app.py              # Main Flask application
├── scraper.py          # Web scraping functionality
├── vertex_client.py    # Vertex AI integration
├── llm_prompt.md       # Prompt template for taxonomy generation
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── templates/          # HTML templates
│   └── index.html
└── terraform/         # Infrastructure as Code
    ├── main.tf            # Provider configuration
    ├── infrastructure.tf  # Base infrastructure setup
    ├── service.tf         # Cloud Run service configuration
    ├── variables.tf       # Variable definitions
    └── terraform.tfvars   # Variable values
```

## Features

- Web scraping using Playwright
- Taxonomy generation using Vertex AI Gemini 1.5 Pro
- CSV output with:
  - Hierarchical category paths
  - Seasonal indicators
  - Confidence ratings
  - Source URLs
  - Reasoning for categorization
- Downloadable results
- User-friendly web interface
