"""Tomahawk2 - Active Security Response & Control

This module provides ACTIVE security capabilities:
- Firewall rule management
- IP blocking/unblocking
- Attack prevention
- Audit logging
- Router configuration
"""

from __future__ import annotations

import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# ============================================================================
# FIREWALL CONTROL
# ============================================================================

def tool_block_ip(ip: str, port: int = 0, protocol: str = "TCP", case: str = "default") -> Dict:
    """Block an IP address using Windows Firewall."""
    try:
        if port > 0:
            rule_name = f"Tomahawk2_Block_{ip}_{port}"
            cmd = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}",
                f"dir=in",
                f"action=block",
                f"remoteip={ip}",
                f"protocol={protocol}",
                f"localport={port}"
            ]
        else:
            rule_name = f"Tomahawk2_Block_{ip}"
            cmd = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}",
                f"dir=in",
                f"action=block",
                f"remoteip={ip}"
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            "status": "success" if result.returncode == 0 else "error",
            "ip": ip,
            "port": port,
            "rule_name": rule_name,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {"status": "error", "ip": ip, "error": str(e)}


def tool_unblock_ip(ip: str, case: str = "default") -> Dict:
    """Unblock an IP address."""
    try:
        # Find and delete the rule
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "delete", "rule", f"remoteip={ip}"],
            capture_output=True, text=True, timeout=30
        )
        
        return {
            "status": "success" if result.returncode == 0 else "error",
            "ip": ip,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {"status": "error", "ip": ip, "error": str(e)}


def tool_list_firewall_rules(case: str = "default") -> Dict:
    """List all firewall rules."""
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
            capture_output=True, text=True, timeout=60
        )
        
        return {
            "status": "success",
            "rules": result.stdout.split('\n')[:100],  # First 100 lines
            "note": "Full output truncated"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ============================================================================
# ROUTER INTEGRATION
# ============================================================================

def tool_router_scan(router_ip: str = "192.168.1.1", case: str = "default") -> Dict:
    """Scan router for connected devices and vulnerabilities."""
    try:
        # ARP scan for devices
        arp_result = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=30)
        
        # Port scan common router ports
        ports = [22, 23, 80, 443, 53, 5000, 8080, 8443]
        open_ports = []
        
        for port in ports:
            try:
                result = subprocess.run(
                    ["Test-NetConnection", "-ComputerName", router_ip, "-Port", str(port)],
                    capture_output=True, text=True, timeout=5
                )
                if "TcpTestSucceeded : True" in result.stdout:
                    open_ports.append(port)
            except:
                pass
        
        return {
            "status": "success",
            "router_ip": router_ip,
            "arp_table": arp_result.stdout.split('\n')[:20],
            "open_ports": open_ports
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ============================================================================
# AUDIT LOGGING
# ============================================================================

def tool_audit_log(action: str, target: str, details: str = "", case: str = "default") -> Dict:
    """Create an audit log entry."""
    log_entry = {
        "time": datetime.now().isoformat(),
        "action": action,
        "target": target,
        "details": details,
        "case": case
    }
    
    # Save to file
    log_path = Path(f"audit_{case}.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return {"status": "logged", "entry": log_entry}


def tool_get_audit_log(case: str = "default", limit: int = 100) -> Dict:
    """Get audit log entries."""
    log_path = Path(f"audit_{case}.jsonl")
    
    if not log_path.exists():
        return {"entries": [], "count": 0}
    
    entries = []
    with open(log_path, "r") as f:
        for line in f:
            entries.append(json.loads(line))
    
    return {
        "entries": entries[-limit:],
        "count": len(entries)
    }


# ============================================================================
# ATTACK PREVENTION
# ============================================================================

def tool_prevent_attack(threat_type: str, source: str, case: str = "default") -> Dict:
    """Take preventive action against detected threats."""
    actions_taken = []
    
    if threat_type in ["bruteforce", "suspicious_ip", "malware"]:
        # Block the IP
        block_result = tool_block_ip(source, case=case)
        actions_taken.append(f"Blocked IP: {source}")
        
        # Log the action
        tool_audit_log("block_ip", source, f"Threat type: {threat_type}", case)
    
    return {
        "status": "prevented",
        "threat_type": threat_type,
        "source": source,
        "actions": actions_taken
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tomahawk2 Active Security Control")
    parser.add_argument("command", choices=["block", "unblock", "rules", "audit", "router"])
    parser.add_argument("--ip", help="IP address to block/unblock")
    parser.add_argument("--port", type=int, default=0, help="Port to block")
    parser.add_argument("--router", default="192.168.1.1", help="Router IP")
    args = parser.parse_args()
    
    if args.command == "block" and args.ip:
        result = tool_block_ip(args.ip, args.port)
    elif args.command == "unblock" and args.ip:
        result = tool_unblock_ip(args.ip)
    elif args.command == "rules":
        result = tool_list_firewall_rules()
    elif args.command == "audit":
        result = tool_get_audit_log()
    elif args.command == "router":
        result = tool_router_scan(args.router)
    
    print(json.dumps(result, indent=2))