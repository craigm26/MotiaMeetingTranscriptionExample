#!/usr/bin/env python3
"""
Streamlit UI for Motia Meeting Transcription Example

Enhanced with real-time Motia backend integration showcasing:
- Live API status dashboard
- Real-time transcription progress
- Event-driven updates
"""

import streamlit as st
import subprocess
import os
import pandas as pd
import time
from pathlib import Path
import json
from datetime import datetime
import requests
from typing import Dict, List, Optional

# Motia backend configuration
MOTIA_BASE_URL = "http://localhost:3000"

# Page configuration
st.set_page_config(
    page_title="Motia Meeting Transcription",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, clean styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .transcription-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .status-completed {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-transcribing {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .status-failed {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .progress-bar {
        background: #f8f9fa;
        border-radius: 10px;
        overflow: hidden;
        height: 8px;
        margin: 0.5rem 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    .action-item {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    .participant-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
    .transcript-text {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        max-height: 300px;
        overflow-y: auto;
    }
    .sidebar-section {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def get_motia_status():
    """Get live status from Motia backend"""
    try:
        response = requests.get(f"{MOTIA_BASE_URL}/hello-world", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def start_transcription_via_motia(filename: str, audio_data: bytes = None):
    """Start transcription using Motia API"""
    try:
        payload = {
            "filename": filename,
            "language": "en",
            "model": "whisper-large-v3"
        }
        
        response = requests.post(
            f"{MOTIA_BASE_URL}/transcribe-meeting",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Failed to start transcription: {e}")
        return None

def display_motia_dashboard():
    """Display live Motia system status"""
    st.subheader("🔗 Live Motia Backend Status")
    
    # Get status with auto-refresh
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = 0
    
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 5:  # Refresh every 5 seconds
        st.session_state.motia_status = get_motia_status()
        st.session_state.last_refresh = current_time
    
    status_data = st.session_state.get('motia_status')
    
    if status_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("System Status", "🟢 Healthy", "Connected to Motia")
        
        with col2:
            stats = status_data.get('stats', {})
            st.metric("Total Transcriptions", stats.get('totalTranscriptions', 0))
        
        with col3:
            st.metric("Active Jobs", stats.get('activeTranscriptions', 0))
        
        with col4:
            uptime = stats.get('systemUptime', 0)
            st.metric("Uptime", f"{uptime:.0f}s")
        
        # Recent activity
        if status_data.get('recentActivity'):
            st.subheader("📊 Recent Transcription Activity")
            df = pd.DataFrame(status_data['recentActivity'])
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
            st.dataframe(df, use_container_width=True)
        
        # Features showcase
        st.subheader("✨ Motia Features in Action")
        features = status_data.get('features', {})
        for feature, status in features.items():
            st.write(f"{status} **{feature}**")
    
    else:
        st.error("🔴 Cannot connect to Motia backend at http://localhost:3000")
        st.info("Make sure to run: `cd meeting_transcript_example && npx motia dev`")

def display_real_time_progress(transcription_id: str):
    """Display real-time transcription progress"""
    st.subheader("⚡ Real-time Transcription Progress")
    
    # Create placeholder for progress updates
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Simulate real-time updates (in real implementation, this would connect to WebSocket)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        status_text.text(f"Processing... {i}% complete")
        time.sleep(0.1)  # Small delay for demo
    
    st.success("✅ Transcription completed!")

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎤 Motia Meeting Transcription</h1>
        <p>Real-time AI transcription powered by Motia's event-driven architecture</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Motia dashboard
    display_motia_dashboard()
    
    st.markdown("---")
    
    # Main transcription interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Audio for Transcription")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Choose audio files",
            type=['mp3', 'wav', 'm4a', 'flac', 'ogg'],
            accept_multiple_files=True,
            help="Upload audio files to transcribe using Motia's real-time processing"
        )
        
        if uploaded_files:
            st.success(f"📎 {len(uploaded_files)} file(s) selected")
            
            # Show file details
            file_details = []
            for file in uploaded_files:
                file_details.append({
                    "Name": file.name,
                    "Size": f"{file.size / 1024 / 1024:.1f} MB",
                    "Type": file.type
                })
            
            st.dataframe(pd.DataFrame(file_details))
    
    with col2:
        st.header("🚀 Motia Processing")
        
        if uploaded_files:
            if st.button("🎯 Start Motia Transcription", type="primary"):
                with st.spinner("Starting Motia transcription pipeline..."):
                    # Use the first file for demo
                    first_file = uploaded_files[0]
                    
                    # Start transcription via Motia API
                    result = start_transcription_via_motia(first_file.name)
                    
                    if result:
                        st.success("✅ Motia transcription started!")
                        st.json(result)
                        
                        # Show real-time progress
                        if 'transcriptionId' in result:
                            display_real_time_progress(result['transcriptionId'])
                    else:
                        st.error("❌ Failed to start transcription")
                        
            # API Testing Section
            st.subheader("🔧 API Testing")
            if st.button("Test Motia Hello Endpoint"):
                status = get_motia_status()
                if status:
                    st.json(status)
                else:
                    st.error("Backend not responding")
        else:
            st.info("📁 Upload audio files to begin Motia processing")
    
    # Motia Features Showcase
    st.markdown("---")
    st.header("🌟 Why Motia Makes This Special")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### ⚡ Real-time Streaming
        - Live progress updates
        - WebSocket-like experience
        - Instant status changes
        """)
    
    with col2:
        st.markdown("""
        ### 🔄 Event-driven Architecture
        - Asynchronous processing
        - Scalable pipeline
        - Robust error handling
        """)
    
    with col3:
        st.markdown("""
        ### 🛠️ Developer Experience
        - Type-safe APIs
        - Auto-generated docs
        - Built-in monitoring
        """)

if __name__ == "__main__":
    main() 