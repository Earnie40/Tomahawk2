# Tomahawk2 Quick Start

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
