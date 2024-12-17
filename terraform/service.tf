# Cloud Run service
resource "google_cloud_run_service" "app" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/categories-app:latest"
        
        resources {
          limits = {
            cpu    = "2000m"    # 2 CPU
            memory = "2048Mi"   # 2GB memory
          }
        }

        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.project_id
        }
      }
      timeout_seconds = 600  # 10 minute timeout
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Make the service public
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.app.location
  project  = google_cloud_run_service.app.project
  service  = google_cloud_run_service.app.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

# Output the URL of the deployed service
output "service_url" {
  value = google_cloud_run_service.app.status[0].url
}
