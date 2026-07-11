"""Tomahawk2 AI Security Monitor Dashboard

A real-time AI-powered security monitoring interface with:
- Live Ring camera feed
- AI facial recognition
- Vehicle detection and license plate recognition
- Email/SMS notifications
- Threat assessment
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import time

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Try to import modules
try:
    from tomahawk2_ai_monitor import AISecurityMonitor
    from tomahawk2_ring import RingIntegration
    from tomahawk2_vision import VisionSystem
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    st.error(f"Missing modules: {e}")


# Page config
st.set_page_config(
    page_title="Tomahawk2 AI Monitor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0a0a0a; color: #ffffff; }
    .stButton>button { background-color: #ff4444; color: white; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; }
    .css-1d391kg { background-color: #1a1a1a; }
    .threat-high { color: #ff4444; font-weight: bold; }
    .threat-medium { color: #ffaa00; font-weight: bold; }
    .threat-low { color: #44ff44; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("🤖 Tomahawk2 AI Security Monitor")
    
    # Initialize session state
    if "monitor_running" not in st.session_state:
        st.session_state.monitor_running = False
    if "threats" not in st.session_state:
        st.session_state.threats = []
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Monitoring controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start Monitor"):
                st.session_state.monitor_running = True
                st.success("Monitor started!")
        with col2:
            if st.button("⏹️ Stop Monitor"):
                st.session_state.monitor_running = False
                st.info("Monitor stopped")
        
        st.markdown("---")
        
        # Configuration
        st.subheader("⚙️ Configuration")
        interval = st.slider("Check Interval (seconds)", 10, 120, 30)
        threshold = st.selectbox("Threat Threshold", ["low", "medium", "high"], index=1)
        
        st.markdown("---")
        
        # Notification settings
        st.subheader("📧 Notifications")
        alert_email = st.text_input("Alert Email", value=os.environ.get("ALERT_EMAIL", ""))
        alert_phone = st.text_input("Alert Phone", value=os.environ.get("ALERT_PHONE", ""))
    
    # Main content
    if st.session_state.monitor_running:
        st.markdown("### 🟢 Monitoring Active")
        
        # Simulate live feed
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("People Detected", "0", "0")
        
        with col2:
            st.metric("Vehicles Detected", "0", "0")
        
        with col3:
            st.metric("Threats Today", len(st.session_state.threats), "0")
        
        st.markdown("---")
        
        # Live analysis placeholder
        st.subheader("📹 Live Camera Feed")
        st.info("Connect your Ring cameras to see live feed here")
        
        # Recent threats
        st.subheader("🚨 Recent Threats")
        if st.session_state.threats:
            for threat in st.session_state.threats[-10:]:
                level = threat.get("threat_level", "unknown")
                css_class = f"threat-{level}"
                st.markdown(f"<p class='{css_class}'>[{level.upper()}] {threat.get('timestamp', 'N/A')}</p>", unsafe_allow_html=True)
        else:
            st.info("No threats detected yet")
    
    else:
        st.info("Click 'Start Monitor' to begin AI-powered security monitoring")
    
    st.markdown("---")
    
    # Image analysis
    st.subheader("🖼️ Image Analysis")
    uploaded_file = st.file_uploader(
        "Upload image for AI analysis",
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("🔍 Analyze with AI"):
            with st.spinner("Analyzing..."):
                # Save temp file
                temp_path = f"/tmp/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Run analysis
                monitor = AISecurityMonitor()
                result = monitor.analyze_frame(temp_path)
                
                st.json(result)
                
                # Add to threats if medium or high
                if result.get("threat_level") in ["medium", "high"]:
                    st.session_state.threats.append(result)
                    st.warning(f"Threat detected: {result.get('threat_level')}")


if __name__ == "__main__":
    main()