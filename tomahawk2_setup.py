"""Tomahawk2 - Complete Setup Script

This script sets up the entire Tomahawk2 cybersecurity system:
- Environment configuration
- GCS bucket creation
- Ring integration setup
- All tools configured
"""

import os
import json
from pathlib import Path

# Create .env file with all required settings
env_content = """# Tomahawk2 Environment Configuration
# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=C:\\Users\\Kyleh\\Downloads\\amazing-thought-446000-p2-720921236d66.json
GCS_BUCKET=tomahawk2-evidence
GCP_PROJECT=amazing-thought-446000-p2

# Ring Security (add your credentials)
RING_EMAIL=
RING_PASSWORD=
RING_TOKEN=

# Ollama
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=qwen2.5-coder:7b

# Security Settings
CASE_DIR=cyber/cases
POSTGRES_DSN=
USE_POSTGRES=false
"""

# Write .env file
Path(".env").write_text(env_content)
print("✅ .env file created")

# Create GCS bucket setup script
gcs_script = """# Google Cloud Storage Setup
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
"""

Path("setup_gcs.sh").write_text(gcs_script)
print("✅ GCS setup script created")

# Create Ring setup instructions
ring_instructions = """# Ring Integration Setup

## Method 1: Using ring-client-api
pip install ring-client-api

## Method 2: Using ring-doorbell
pip install ring-doorbell

## To get your Ring credentials:
1. Use your Ring account email and password
2. You'll receive a 2FA code on your phone
3. Enter the code when prompted

## Test Ring connection:
python -c "
from tomahawk2_ring import tool_ring_auth
import json
print(json.dumps(tool_ring_auth(email='your@email.com', password='your_password'), indent=2))
"
"""

Path("RING_SETUP.md").write_text(ring_instructions)
print("✅ Ring setup instructions created")

# Create quick start script
quick_start = """# Tomahawk2 Quick Start

## 1. Security Scan
python tomahawk2_agent.py "Scan my PC for malware"

## 2. Entry Point Analysis
python -c "from tomahawk2_agent import tool_check_entry_points; import json; print(json.dumps(tool_check_entry_points(), indent=2))"

## 3. Network Devices
python -c "from tomahawk2_agent import tool_scan_network_devices; import json; print(json.dumps(tool_scan_network_devices(), indent=2))"

## 4. Vehicle/Camera Analysis
python tomahawk2_vision.py /path/to/image.jpg --mode vehicle

## 5. ALPR Camera Detection
python tomahawk2_vision.py /path/to/image.jpg --mode alpr --location "Downtown"

## 6. Upload to GCS
python -c "from tomahawk2_agent import tool_upload_to_gcs; import json; print(json.dumps(tool_upload_to_gcs('tomahawk2-evidence', '/path/to/file'), indent=2))"

## 7. Use qwen2.5-coder:32b in Colab
https://colab.research.google.com/github/Earnie40/Tomahawk2
"""

Path("QUICK_START.md").write_text(quick_start)
print("✅ Quick start guide created")

print("\n🎉 Tomahawk2 is fully set up!")
print("\nNext steps:")
print("1. Add your Ring credentials to .env")
print("2. Run: gcloud auth activate-service-account --key-file=amazing-thought-446000-p2-720921236d66.json")
print("3. Run: gsutil mb -p amazing-thought-446000-p2 gs://tomahawk2-evidence")
print("4. Start using the tools!")