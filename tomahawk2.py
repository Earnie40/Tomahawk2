"""Tomahawk2 - Advanced Agentic Cybersecurity & Forensic Investigator
Main Entry Point

This is the complete cybersecurity system for:
- Malware/spyware detection
- Digital fingerprint tracking
- Continuous monitoring (PC, mobile, Google accounts)
- Security camera integration (Ring)
- Vehicle AI vision (ALPR, vehicle detection)
- Flock/ALPR camera detection
"""

import argparse
import json
import sys
from pathlib import Path

# Import all modules
from tomahawk2_agent import Tomahawk2Agent, tool_scan_malware, tool_check_entry_points, tool_scan_network_devices
from tomahawk2_vision import tool_vehicle_analyze, tool_vision_analyze, tool_alpr_detect
from tomahawk2_monitor import tool_start_monitor, tool_stop_monitor
from tomahawk2_ring import tool_ring_auth, tool_ring_list_cameras, tool_ring_events
from tomahawk2_control import tool_block_ip, tool_unblock_ip, tool_prevent_attack, tool_audit_log
from tomahawk2_ai_monitor import tool_ai_monitor_start, tool_ai_monitor_stop, tool_ai_analyze_image


def main():
    parser = argparse.ArgumentParser(
        description="Tomahawk2 - Advanced Agentic Cybersecurity & Forensic Investigator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tomahawk2.py scan                    # Run security scan
  python tomahawk2.py monitor --once          # Single monitoring check
  python tomahawk2.py vision /path/to/image   # Analyze image
  python tomahawk2.py alpr /path/to/image     # Detect ALPR cameras
  python tomahawk2.py ring                     # Ring camera status
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Run security scan")
    scan_parser.add_argument("--path", default=".", help="Path to scan")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Continuous monitoring")
    monitor_parser.add_argument("--once", action="store_true", help="Run once and exit")
    monitor_parser.add_argument("--interval", type=int, default=60, help="Check interval")
    monitor_parser.add_argument("--gcs-bucket", default="", help="GCS bucket")
    
    # Vision command
    vision_parser = subparsers.add_parser("vision", help="Analyze image")
    vision_parser.add_argument("image", help="Image file to analyze")
    
    # ALPR command
    alpr_parser = subparsers.add_parser("alpr", help="ALPR camera detection")
    alpr_parser.add_argument("image", help="Image file to analyze")
    alpr_parser.add_argument("--location", default="", help="Location")
    
# Ring command
    ring_parser = subparsers.add_parser("ring", help="Ring camera integration")
    
    # AI Monitor commands
    ai_parser = subparsers.add_parser("ai", help="AI security monitoring")
    ai_parser.add_argument("action", choices=["start", "stop"], help="Start or stop AI monitor")
    ai_parser.add_argument("--interval", type=int, default=30, help="Check interval")
    
    # Control commands
    control_parser = subparsers.add_parser("block", help="Block IP address")
    control_parser.add_argument("ip", help="IP address to block")
    control_parser.add_argument("--port", type=int, default=0, help="Port to block")
    
    unblock_parser = subparsers.add_parser("unblock", help="Unblock IP address")
    unblock_parser.add_argument("ip", help="IP address to unblock")
    
    prevent_parser = subparsers.add_parser("prevent", help="Prevent attack")
    prevent_parser.add_argument("threat_type", help="Threat type")
    prevent_parser.add_argument("source", help="Source IP")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        print("🔍 Running security scan...")
        malware = tool_scan_malware(args.path)
        entry = tool_check_entry_points()
        network = tool_scan_network_devices()
        
        result = {
            "malware_scan": malware,
            "entry_points": entry,
            "network_devices": network
        }
        print(json.dumps(result, indent=2))
    
    elif args.command == "monitor":
        if args.once:
            from tomahawk2_monitor import ContinuousMonitor
            monitor = ContinuousMonitor(gcs_bucket=args.gcs_bucket)
            monitor._check_pc_security()
            monitor._check_network()
            monitor._save_events()
            print("✅ Single monitoring check completed")
        else:
            print(f"🛡️ Starting continuous monitor (interval: {args.interval}s)...")
            tool_start_monitor(interval=args.interval, gcs_bucket=args.gcs_bucket)
    
    elif args.command == "vision":
        print(f"👁️ Analyzing image: {args.image}")
        result = tool_vehicle_analyze(args.image)
        print(json.dumps(result, indent=2))
    
    elif args.command == "alpr":
        print(f"🚗 Detecting ALPR cameras in: {args.image}")
        result = tool_alpr_detect(args.image, args.location)
        print(json.dumps(result, indent=2))
    
    elif args.command == "ring":
        print("📹 Ring camera status...")
        result = tool_ring_list_cameras()
        print(json.dumps(result, indent=2))
    
    elif args.command == "block":
        print(f"🚫 Blocking IP: {args.ip}")
        result = tool_block_ip(args.ip, args.port)
        print(json.dumps(result, indent=2))
    
    elif args.command == "unblock":
        print(f"✅ Unblocking IP: {args.ip}")
        result = tool_unblock_ip(args.ip)
        print(json.dumps(result, indent=2))
    
    elif args.command == "ai":
        if args.action == "start":
            print(f"🤖 Starting AI security monitor (interval: {args.interval}s)...")
            result = tool_ai_monitor_start(interval=args.interval)
            print(json.dumps(result, indent=2))
        else:
            print("🛑 Stopping AI security monitor...")
            result = tool_ai_monitor_stop()
            print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()