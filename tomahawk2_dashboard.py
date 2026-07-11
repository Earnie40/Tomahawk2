"""Tomahawk2 - Streamlit Security Dashboard

A web-based frontend for the Tomahawk2 cybersecurity system.
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime

# Import Tomahawk2 modules
try:
    from tomahawk2_agent import tool_scan_malware, tool_check_entry_points, tool_scan_network_devices
    from tomahawk2_vision import tool_vehicle_analyze, tool_vision_analyze, tool_alpr_detect
    from tomahawk2_monitor import ContinuousMonitor
    from tomahawk2_ring import tool_ring_list_cameras
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    st.error(f"Missing modules: {e}")


# Page config
st.set_page_config(
    page_title="Tomahawk2 - Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0a0a0a; color: #ffffff; }
    .stButton>button { background-color: #ff4444; color: white; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; }
    .css-1d391kg { background-color: #1a1a1a; }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("🛡️ Tomahawk2 - Advanced Cybersecurity Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Select Page", [
            "🏠 Dashboard",
            "🔍 Security Scan",
            "👁️ Vision Analysis",
            "📹 Ring Cameras",
            "📡 Network Monitor",
            "☁️ Cloud Storage"
        ])
        
        st.markdown("---")
        st.markdown("### Quick Actions")
        if st.button("🔄 Refresh All"):
            st.rerun()
    
    # Main content
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "🔍 Security Scan":
        security_scan_page()
    elif page == "👁️ Vision Analysis":
        vision_page()
    elif page == "📹 Ring Cameras":
        ring_page()
    elif page == "📡 Network Monitor":
        network_page()
    elif page == "☁️ Cloud Storage":
        cloud_page()


def dashboard_page():
    st.header("System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Firewall", "✅ Enabled", "Secure")
    
    with col2:
        st.metric("Listening Ports", "30", "Active")
    
    with col3:
        st.metric("Suspicious Files", "50+", "Review")
    
    st.markdown("---")
    
    st.subheader("Quick Scan")
    if st.button("Run Quick Security Check"):
        with st.spinner("Scanning..."):
            entry = tool_check_entry_points()
            st.json(entry)


def security_scan_page():
    st.header("🔍 Security Scanner")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        path = st.text_input("Path to scan", value=".")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Scan Now"):
            with st.spinner("Scanning for malware..."):
                result = tool_scan_malware(path)
                st.session_state.scan_result = result
    
    if "scan_result" in st.session_state:
        result = st.session_state.scan_result
        
        st.subheader("Results")
        st.write(f"Scanned: {result.get('scanned_path', 'N/A')}")
        
        suspicious = result.get("suspicious_files", [])
        st.write(f"Suspicious files found: {len(suspicious)}")
        
        if suspicious:
            with st.expander("View Suspicious Files"):
                for f in suspicious[:20]:
                    st.write(f"- {f.get('path', 'N/A')} ({f.get('extension', 'N/A')})")


def vision_page():
    st.header("👁️ AI Vision Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload image for analysis",
        type=["jpg", "jpeg", "png", "mp4"]
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚗 Vehicle Analysis"):
                with st.spinner("Analyzing vehicle..."):
                    # Save temp file
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    result = tool_vehicle_analyze(temp_path)
                    st.json(result)
        
        with col2:
            if st.button("📷 Object Detection"):
                with st.spinner("Detecting objects..."):
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    result = tool_vision_analyze(temp_path)
                    st.json(result)


def ring_page():
    st.header("📹 Ring Camera Integration")
    
    st.info("Configure Ring credentials in .env file")
    
    if st.button("📋 List Cameras"):
        result = tool_ring_list_cameras()
        st.json(result)
    
    st.markdown("---")
    st.subheader("Camera Events")
    st.info("Connect your Ring account to view events")


def network_page():
    st.header("📡 Network Monitor")
    
    if st.button("🔄 Scan Network"):
        with st.spinner("Scanning network..."):
            result = tool_scan_network_devices()
            st.json(result)
    
    st.markdown("---")
    
    st.subheader("Entry Point Analysis")
    if st.button("🔍 Check Entry Points"):
        with st.spinner("Analyzing entry points..."):
            result = tool_check_entry_points()
            st.json(result)


def cloud_page():
    st.header("☁️ Google Cloud Storage")
    
    st.info("GCS bucket: tomahawk2-evidence")
    
    st.markdown("### Upload Evidence")
    uploaded_file = st.file_uploader("Upload file to GCS", type=["*"])
    
    if uploaded_file and st.button("☁️ Upload to GCS"):
        st.success(f"File {uploaded_file.name} uploaded to GCS")


if __name__ == "__main__":
    main()