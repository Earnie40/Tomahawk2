# Tomahawk2 - Advanced Agentic Cybersecurity & Forensic Investigator

## Project Overview
An AI-powered cybersecurity agent that provides comprehensive threat detection, continuous monitoring, and AI vision analysis for:
- **Malware/Spyware Detection** - System scanning, IOC extraction, entry point analysis
- **Digital Fingerprint Tracking** - Network, process, and file analysis
- **Continuous Monitoring** - PC, mobile, and Google account security
- **Security Camera Integration** - Ring, ALPR, and general surveillance
- **Vehicle AI Vision** - License plate recognition, vehicle identification
- **Flock/ALPR Detection** - Find and log surveillance cameras

## Architecture

### Core Components
1. **Threat Detection Engine** - IOC extraction, malware scanning, entry point analysis
2. **Continuous Monitor** - Real-time PC, mobile, and account monitoring
3. **Vision System** - AI-powered camera analysis for vehicles, security, ALPR
4. **Evidence Management** - Tamper-evident custody ledger (existing)
5. **Cloud Integration** - GCS storage, Google account security
6. **Reporting** - Automated security reports

## Quick Start

### Using qwen2.5-coder:32b in Google Colab (Free GPU)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Earnie40/Tomahawk2/blob/main/qwen2.5-coder-32b-colab.ipynb)

## Features

### 1. Threat Detection
- Malware/spyware scanning
- IOC extraction (IPs, domains, hashes, CVEs)
- Entry point analysis
- Digital fingerprint tracking
- Process analysis

### 2. Continuous Monitoring
- Local PC security monitoring
- Mobile device security (Android/iOS)
- Google account security
- Ring security system integration

### 3. AI Vision System
- Vehicle dash/proximity camera analysis
- License plate recognition (ALPR)
- Vehicle make/model/year/color detection
- Person/object/animal identification
- Flock/ALPR camera detection
- Security camera analysis

### 4. Cloud Integration
- Google Cloud Storage for evidence
- Automated upload of findings
- Secure cloud storage

## Installation

```bash
# Clone the repository
git clone https://github.com/Earnie40/Tomahawk2.git
cd Tomahawk2

# Install core dependencies
pip install -r requirements_tomahawk2.txt

# For full vision features (optional)
pip install opencv-python ultralytics easyocr

# Build the Ollama model (or use in Colab)
ollama create -f cyber/Modelfile cyber-investigator
```

## Usage

```bash
# Run a security investigation
python tomahawk2_agent.py "Scan my PC for malware and check for entry points"

# Analyze an image
python tomahawk2_vision.py /path/to/image.jpg --mode vehicle

# Interactive chat mode
python cyber/agent.py --case security_scan chat

# Use with qwen2.5-coder:32b in Colab
# Open the notebook and run all cells
```

## AI Security Monitor

Real-time AI-powered security monitoring with:
- Person/vehicle detection using YOLO
- License plate recognition (ALPR)
- Facial recognition
- Email/SMS notifications for threats
- Continuous background monitoring

```bash
# Start AI monitoring
python tomahawk2.py ai start --interval 30

# Stop AI monitoring
python tomahawk2.py ai stop

# Analyze an image
python tomahawk2.py vision /path/to/image.jpg
```

## File Structure

- `tomahawk2.py` - Main CLI entry point
- `tomahawk2_agent.py` - Main agent with threat detection and monitoring tools
- `tomahawk2_vision.py` - AI vision system for ALPR and vehicle analysis
- `tomahawk2_ai_monitor.py` - AI security monitoring with real-time threat detection
- `tomahawk2_ai_dashboard.py` - Streamlit web interface for AI monitoring
- `tomahawk2_dashboard.py` - Main Streamlit dashboard
- `tomahawk2_ring.py` - Ring camera integration
- `qwen2.5-coder-32b-colab.ipynb` - Colab notebook for 32b model
- `requirements_tomahawk2.txt` - Python dependencies
- `cyber/` - Existing forensic investigation tools

## License
MIT License