# Google Cloud Storage Setup
# Run this in Cloud Shell or with gcloud installed

# Set project
gcloud config set project amazing-thought-446000-p2

# Create bucket for evidence
gsutil mb -p amazing-thought-446000-p2 gs://tomahawk2-evidence

# Enable APIs
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudfunctions.googleapis.com

# Set up service account for Tomahawk2
gcloud iam service-accounts create tomahawk2-agent --display-name="Tomahawk2 Security Agent"
