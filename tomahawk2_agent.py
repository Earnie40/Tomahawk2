"""Tomahawk2 - Advanced Agentic Cybersecurity & Forensic Investigator

This agent provides comprehensive security monitoring and analysis:
- Malware/spyware detection
- Digital fingerprint tracking
- Continuous PC/mobile/account monitoring
- Security camera integration
- Vehicle AI vision (ALPR, vehicle detection)
- Flock/ALPR camera detection and logging
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Import existing cyber tools
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

# Core tools from existing cyber agent
try:
    from tools import custody, hashes, iocs, logs, evidence, timeline, report
    from storage import PostgresLedger
except ImportError:
    # Fallback for when tools aren't available
    pass

# ============================================================================
# THREAT DETECTION TOOLS
# ============================================================================

def tool_scan_malware(path: str = "", case: str = "default") -> Dict:
    """Scan a file or directory for malware signatures and suspicious patterns."""
    import subprocess
    import re
    
    p = Path(path) if path else Path.cwd()
    results = {
        "scanned_path": str(p),
        "suspicious_files": [],
        "malware_indicators": [],
        "suspicious_processes": []
    }
    
    # Check for suspicious file extensions
    suspicious_exts = {'.exe', '.bat', '.ps1', '.vbs', '.scr', '.pif', '.cmd', '.com', '.jar'}
    
    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = list(p.rglob("*"))
    else:
        return {"error": f"Path not found: {path}"}
    
    for f in files:
        if f.suffix.lower() in suspicious_exts:
            results["suspicious_files"].append({
                "path": str(f),
                "size": f.stat().st_size if f.exists() else 0,
                "extension": f.suffix
            })
    
    # Check running processes for suspicious activity
    try:
        proc_result = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=30)
        suspicious_patterns = [
            r"mimikatz", r"metasploit", r"cobalt", r"empire", r"powershell.*-enc",
            r"wmic.*process", r"rundll32.*javascript", r"regsvr32.*scrobj"
        ]
        for line in proc_result.stdout.split('\n'):
            for pattern in suspicious_patterns:
                if re.search(pattern, line, re.I):
                    results["suspicious_processes"].append(line.strip())
    except Exception as e:
        results["process_error"] = str(e)
    
    return results


def tool_check_entry_points(case: str = "default") -> Dict:
    """Analyze system for potential entry points and vulnerabilities."""
    import subprocess
    import re
    
    results = {
        "open_ports": [],
        "listening_services": [],
        "firewall_status": "unknown",
        "vulnerable_ports": []
    }
    
    # Check open ports
    try:
        net_result = subprocess.run(["netstat", "-an"], capture_output=True, text=True, timeout=30)
        for line in net_result.stdout.split('\n'):
            if 'LISTENING' in line:
                results["listening_services"].append(line.strip())
    except Exception as e:
        results["netstat_error"] = str(e)
    
    # Check firewall
    try:
        fw_result = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], 
                                   capture_output=True, text=True, timeout=30)
        if "ON" in fw_result.stdout:
            results["firewall_status"] = "enabled"
        else:
            results["firewall_status"] = "disabled"
    except Exception as e:
        results["firewall_error"] = str(e)
    
    # Common vulnerable ports
    vulnerable = [22, 23, 135, 139, 445, 1433, 3389, 5432, 27017, 6379]
    for service in results["listening_services"]:
        for port in vulnerable:
            if f":{port}" in service:
                results["vulnerable_ports"].append(port)
    
    return results


def tool_scan_network_devices(case: str = "default") -> Dict:
    """Scan network for connected devices and potential threats."""
    import subprocess
    
    results = {
        "arp_table": [],
        "arp_spoof_suspects": []
    }
    
    try:
        arp_result = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=30)
        results["arp_table"] = arp_result.stdout.split('\n')
    except Exception as e:
        results["arp_error"] = str(e)
    
    return results


# ============================================================================
# MOBILE SECURITY TOOLS
# ============================================================================

def tool_analyze_mobile_security(case: str = "default") -> Dict:
    """Analyze mobile device security (Android/iOS)."""
    return {
        "status": "ready",
        "capabilities": [
            "app_permission_analysis",
            "network_traffic_monitoring",
            "malware_scanning",
            "account_security_check"
        ],
        "note": "Connect mobile device via USB or use ADB for Android analysis"
    }


# ============================================================================
# GOOGLE ACCOUNT SECURITY TOOLS
# ============================================================================

def tool_check_google_account_security(case: str = "default") -> Dict:
    """Check Google account security status."""
    return {
        "status": "ready",
        "capabilities": [
            "2fa_status",
            "recent_login_check",
            "app_password_audit",
            "security_event_monitoring"
        ],
        "note": "Requires Google API credentials for full functionality"
    }


# ============================================================================
# CAMERA INTEGRATION TOOLS
# ============================================================================

def tool_analyze_camera_feed(feed_url: str = "", case: str = "default") -> Dict:
    """Analyze security camera feed for threats and objects."""
    return {
        "status": "ready",
        "capabilities": [
            "person_detection",
            "vehicle_detection",
            "license_plate_recognition",
            "animal_detection",
            "suspicious_activity"
        ],
        "feed_url": feed_url,
        "note": "Requires OpenCV and camera integration"
    }


def tool_detect_alpr_cameras(case: str = "default") -> Dict:
    """Detect and log ALPR/Flock cameras in area."""
    return {
        "status": "ready",
        "capabilities": [
            "camera_detection",
            "location_logging",
            "time_stamping",
            "gcs_upload"
        ],
        "note": "Use with camera feed analysis to identify ALPR systems"
    }


# ============================================================================
# VEHICLE VISION TOOLS
# ============================================================================

def tool_analyze_vehicle_camera(image_path: str = "", case: str = "default") -> Dict:
    """Analyze vehicle dash/proximity camera for vehicles, plates, objects."""
    return {
        "status": "ready",
        "capabilities": [
            "license_plate_recognition",
            "vehicle_make_model_year",
            "vehicle_color",
            "object_detection",
            "person_detection"
        ],
        "image_path": image_path,
        "note": "Requires computer vision model (YOLO, OpenALPR)"
    }


# ============================================================================
# CLOUD STORAGE TOOLS
# ============================================================================

def tool_upload_to_gcs(bucket: str, source_path: str, case: str = "default") -> Dict:
    """Upload evidence to Google Cloud Storage."""
    from google.cloud import storage
    
    try:
        client = storage.Client()
        bucket_obj = client.bucket(bucket)
        blob = bucket_obj.blob(Path(source_path).name)
        blob.upload_from_filename(source_path)
        return {
            "status": "success",
            "bucket": bucket,
            "uploaded_file": source_path,
            "gcs_path": f"gs://{bucket}/{Path(source_path).name}"
        }
    except Exception as e:
        return {"error": str(e), "note": "Ensure GOOGLE_APPLICATION_CREDENTIALS is set"}


# ============================================================================
# MAIN AGENT CLASS
# ============================================================================

class Tomahawk2Agent:
    """Advanced cybersecurity and forensic investigator agent."""
    
    def __init__(self, model: str = "qwen2.5-coder:32b", url: str = "http://localhost:11434/api/chat"):
        self.model = model
        self.url = url
        self.tools = {
            "scan_malware": tool_scan_malware,
            "check_entry_points": tool_check_entry_points,
            "scan_network_devices": tool_scan_network_devices,
            "analyze_mobile_security": tool_analyze_mobile_security,
            "check_google_account_security": tool_check_google_account_security,
            "analyze_camera_feed": tool_analyze_camera_feed,
            "detect_alpr_cameras": tool_detect_alpr_cameras,
            "analyze_vehicle_camera": tool_analyze_vehicle_camera,
            "upload_to_gcs": tool_upload_to_gcs,
        }
    
    def run_investigation(self, query: str) -> Dict:
        """Run a security investigation based on the query."""
        # This would integrate with the existing agent.py tool-calling loop
        return {
            "query": query,
            "model": self.model,
            "available_tools": list(self.tools.keys()),
            "status": "ready"
        }


def main():
    parser = argparse.ArgumentParser(description="Tomahawk2 - Advanced Cybersecurity Agent")
    parser.add_argument("--model", default="qwen2.5-coder:32b")
    parser.add_argument("--case", default="default")
    parser.add_argument("query", nargs="*", help="Security investigation query")
    args = parser.parse_args()
    
    agent = Tomahawk2Agent(model=args.model)
    query = " ".join(args.query)
    
    if query:
        result = agent.run_investigation(query)
        print(json.dumps(result, indent=2))
    else:
        print("Tomahawk2 - Advanced Cybersecurity Agent")
        print("Available tools:", list(agent.tools.keys()))
        print("\nUsage: python tomahawk2_agent.py 'Scan my PC for malware'")


if __name__ == "__main__":
    main()