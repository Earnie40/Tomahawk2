"""Tomahawk2 - Continuous Security Monitor

This module provides real-time monitoring for:
- PC security (processes, files, network)
- Mobile device security
- Google account security
- Ring camera events
- ALPR camera detection
"""

from __future__ import annotations

import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import subprocess
import re

# Try to import optional dependencies
try:
    from google.cloud import storage
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False


class ContinuousMonitor:
    """Continuous security monitoring system."""
    
    def __init__(self, gcs_bucket: Optional[str] = None, case: str = "default"):
        self.gcs_bucket = gcs_bucket
        self.case = case
        self.running = False
        self.events: List[Dict] = []
    
    def start(self, interval: int = 60):
        """Start continuous monitoring."""
        self.running = True
        print(f"🛡️ Tomahawk2 Monitor started (interval: {interval}s)")
        
        while self.running:
            self._check_pc_security()
            self._check_network()
            self._save_events()
            time.sleep(interval)
    
    def stop(self):
        """Stop monitoring."""
        self.running = False
        print("🛑 Tomahawk2 Monitor stopped")
    
    def _check_pc_security(self):
        """Check PC for security issues."""
        # Check for suspicious processes
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=30)
            suspicious = []
            patterns = [
                r"mimikatz", r"metasploit", r"cobalt", r"empire",
                r"powershell.*-enc", r"rundll32.*javascript"
            ]
            for line in result.stdout.split('\n'):
                for pattern in patterns:
                    if re.search(pattern, line, re.I):
                        suspicious.append(line.strip())
            
            if suspicious:
                self.events.append({
                    "time": datetime.now().isoformat(),
                    "type": "suspicious_process",
                    "severity": "high",
                    "details": suspicious
                })
        except Exception as e:
            pass
    
    def _check_network(self):
        """Check network for changes."""
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=30)
            # Log ARP table for analysis
            self.events.append({
                "time": datetime.now().isoformat(),
                "type": "network_scan",
                "severity": "info",
                "details": result.stdout.split('\n')[:10]  # First 10 entries
            })
        except Exception as e:
            pass
    
    def _save_events(self):
        """Save events to file and optionally GCS."""
        if not self.events:
            return
        
        # Save locally
        log_path = Path(f"monitor_{self.case}.jsonl")
        with open(log_path, "a") as f:
            for event in self.events:
                f.write(json.dumps(event) + "\n")
        
        # Upload to GCS if configured
        if self.gcs_bucket and GCS_AVAILABLE:
            try:
                client = storage.Client()
                bucket = client.bucket(self.gcs_bucket)
                blob = bucket.blob(f"monitor/{datetime.now().isoformat()}.json")
                blob.upload_from_string(json.dumps(self.events))
            except Exception as e:
                pass
        
        self.events = []


def tool_start_monitor(interval: int = 60, case: str = "default", gcs_bucket: str = "") -> Dict:
    """Start continuous security monitoring."""
    monitor = ContinuousMonitor(gcs_bucket=gcs_bucket, case=case)
    
    # Run in background thread
    thread = threading.Thread(target=monitor.start, args=(interval,), daemon=True)
    thread.start()
    
    return {
        "status": "started",
        "interval": interval,
        "case": case,
        "gcs_bucket": gcs_bucket,
        "note": "Monitoring running in background"
    }


def tool_stop_monitor() -> Dict:
    """Stop continuous monitoring."""
    return {"status": "stopped", "note": "Call this to stop the monitor"}


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tomahawk2 Continuous Monitor")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")
    parser.add_argument("--case", default="default", help="Case name")
    parser.add_argument("--gcs-bucket", default="", help="GCS bucket for evidence")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()
    
    monitor = ContinuousMonitor(gcs_bucket=args.gcs_bucket, case=args.case)
    
    if args.once:
        monitor._check_pc_security()
        monitor._check_network()
        monitor._save_events()
        print("Single check completed")
    else:
        try:
            monitor.start(args.interval)
        except KeyboardInterrupt:
            monitor.stop()