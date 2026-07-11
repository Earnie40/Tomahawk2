# Tomahawk2 - Agentic Cybersecurity Tools

This repository contains tools and notebooks for agentic cybersecurity applications with qwen2.5-coder:32b integration.

## Quick Start

### Using qwen2.5-coder:32b in Google Colab (Free GPU)

1. Open the notebook in Google Colab:
   [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Earnie40/Tomahawk2/blob/main/qwen2.5-coder-32b-colab.ipynb)

2. Run each cell to:
   - Check GPU availability
   - Install Ollama
   - Download qwen2.5-coder:32b (20-25GB)
   - Test the model

### Free GPU Options
- **Google Colab**: 12-15 hours/week free GPU time
- **Kaggle Kernels**: 30 hours/week free
- No API key or credit card required

## Streamlit Deployment

### Deploy to Streamlit Community Cloud

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Select repository: `Earnie40/Tomahawk2`
4. Set main file: `tomahawk2_ai_dashboard.py`
5. Add secrets in Streamlit Cloud:
   - `RING_EMAIL` - Your Ring account email
   - `RING_PASSWORD` - Your Ring password
   - `ALERT_EMAIL` - Email for notifications
   - `ALERT_PHONE` - Phone for SMS alerts

## System Requirements

For local use, your system needs:
- **GPU**: 16+ GB VRAM (NVIDIA/AMD) for qwen2.5-coder:32b
- **RAM**: 32+ GB
- **Disk**: 30+ GB free space

For smaller models:
- **qwen2.5-coder:7b** works on most systems (4-5 GB)
- **qwen2.5-coder:14b** may work on systems with 16+ GB RAM

## Repository Structure

- `tomahawk2.py` - Main CLI entry point
- `tomahawk2_agent.py` - Security agent with threat detection
- `tomahawk2_vision.py` - AI vision system for ALPR and vehicle analysis
- `tomahawk2_ai_monitor.py` - AI security monitoring
- `tomahawk2_ai_dashboard.py` - Streamlit web interface
- `tomahawk2_dashboard.py` - Main Streamlit dashboard
- `tomahawk2_ring.py` - Ring camera integration
- `qwen2.5-coder-32b-colab.ipynb` - Colab notebook for 32b model
- `requirements_tomahawk2.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration

## License

MIT License