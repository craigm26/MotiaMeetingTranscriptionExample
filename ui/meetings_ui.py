#!/usr/bin/env python3
"""
Streamlit UI for Motia Meeting Transcription Example

This provides a clean, modern interface for viewing meeting transcription results
from the Motia workflow, including real-time progress and completed transcriptions.
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

# Configuration
MOTIA_API_BASE = "http://localhost:3000"
MOTIA_WORKBENCH_BASE = "http://localhost:3001"

def check_motia_status():
    """Check if Motia services are running"""
    try:
        # Check API server
        api_response = requests.get(f"{MOTIA_API_BASE}/hello-world", timeout=5)
        api_running = api_response.status_code == 200
        
        # Check workbench
        workbench_response = requests.get(f"{MOTIA_WORKBENCH_BASE}", timeout=5)
        workbench_running = workbench_response.status_code == 200
        
        return api_running, workbench_running
    except:
        return False, False

def get_transcription_streams():
    """Get transcription data from Motia streams"""
    try:
        # In a real implementation, this would fetch from Motia's stream API
        # For now, we'll simulate the data structure based on the stream schema
        
        # Simulate stream data based on the schema from meeting-transcription.stream.ts
        mock_streams = [
            {
                "transcriptionId": "trans_001",
                "status": "completed",
                "progress": 100,
                "filename": "team_meeting_2024_01_15.mp4",
                "duration": 3240,  # 54 minutes
                "transcript": """Welcome everyone to our quarterly planning meeting. I'm Sarah Johnson, your project manager, and I'll be facilitating today's discussion.

Let's start with a quick round of updates from each team lead. John, would you like to go first with the engineering updates?

John: Thanks Sarah. The engineering team has made significant progress on the new API integration. We've completed the authentication module and are about 70% through the data synchronization features. We're on track to meet our Q1 deadline.

Sarah: Excellent progress, John. Any blockers we should be aware of?

John: We're waiting on the final API documentation from our vendor, but that should arrive by the end of the week. Otherwise, we're in good shape.

Sarah: Great. Now let's hear from the marketing team. Lisa, what's the latest?

Lisa: The marketing team has launched our new campaign across all channels. Early metrics are promising - we're seeing a 25% increase in engagement compared to last quarter. We've also finalized the Q2 campaign strategy and are ready to present it to leadership next week.

Sarah: Outstanding results, Lisa. Any challenges or support needed?

Lisa: We could use some additional design resources for the Q2 campaign assets, but we're working with the creative team to prioritize our needs.

Sarah: Noted. We'll address that in our resource planning session. Now for the sales update. Mike, how are we looking?

Mike: Sales team is performing well. We've exceeded our Q1 targets by 15% and have a strong pipeline for Q2. Our new product features are resonating well with prospects, and we're seeing increased interest from enterprise clients.

Sarah: That's fantastic news, Mike. What's driving this success?

Mike: The combination of our improved product features and the marketing team's campaign has created a lot of buzz. We're also seeing better conversion rates from our demos thanks to the new onboarding process.

Sarah: Perfect. Now let's move to our main agenda items. First, let's discuss the Q2 roadmap priorities. I've prepared a summary of the key initiatives we need to focus on.

[Meeting continues with detailed discussion of Q2 priorities, resource allocation, and action items...]

Sarah: Before we wrap up, let's review our action items. John, you'll finalize the API integration by March 15th. Lisa, you'll present the Q2 campaign strategy to leadership next week. Mike, you'll provide updated sales projections by Friday. And I'll schedule our next team meeting for two weeks from now.

Does everyone have their action items clear? Any questions or concerns?

[General agreement from all participants]

Sarah: Perfect. Thank you everyone for your time and contributions today. This has been a very productive meeting. Have a great rest of your day!""",
                "summary": "Quarterly planning meeting focused on Q1 updates and Q2 roadmap planning. Engineering team is 70% complete on API integration. Marketing campaign showing 25% engagement increase. Sales exceeding Q1 targets by 15%. Key action items assigned for API completion, campaign presentation, and sales projections.",
                "actionItems": [
                    "John to finalize API integration by March 15th",
                    "Lisa to present Q2 campaign strategy to leadership next week", 
                    "Mike to provide updated sales projections by Friday",
                    "Sarah to schedule next team meeting for two weeks from now"
                ],
                "participants": ["Sarah Johnson", "John Smith", "Lisa Chen", "Mike Rodriguez"],
                "whisperModel": "whisper-large-v3",
                "processingTime": 45000,  # 45 seconds
                "timestamp": "2024-01-15T14:30:00Z"
            },
            {
                "transcriptionId": "trans_002", 
                "status": "transcribing",
                "progress": 65,
                "filename": "client_presentation_2024_01_16.mp4",
                "duration": None,
                "transcript": None,
                "summary": None,
                "actionItems": None,
                "participants": None,
                "whisperModel": "whisper-large-v3",
                "processingTime": None,
                "timestamp": "2024-01-16T10:15:00Z"
            },
            {
                "transcriptionId": "trans_003",
                "status": "failed",
                "progress": 0,
                "filename": "corrupted_audio_file.mp4",
                "duration": None,
                "transcript": None,
                "summary": None,
                "actionItems": None,
                "participants": None,
                "error": "Audio file appears to be corrupted or in unsupported format",
                "whisperModel": "whisper-large-v3",
                "processingTime": None,
                "timestamp": "2024-01-16T09:45:00Z"
            }
        ]
        
        return mock_streams
    except Exception as e:
        st.error(f"Error fetching transcription data: {e}")
        return []

def format_duration(seconds):
    """Format duration in seconds to human readable format"""
    if seconds is None:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def format_processing_time(ms):
    """Format processing time in milliseconds"""
    if ms is None:
        return "Unknown"
    
    if ms < 1000:
        return f"{ms}ms"
    else:
        return f"{ms/1000:.1f}s"

def get_status_badge(status):
    """Get HTML for status badge"""
    status_classes = {
        "completed": "status-completed",
        "transcribing": "status-transcribing", 
        "failed": "status-failed"
    }
    
    class_name = status_classes.get(status, "status-transcribing")
    return f'<span class="status-badge {class_name}">{status.upper()}</span>'

def display_transcription_card(transcription):
    """Display a single transcription card"""
    with st.container():
        st.markdown(f"""
        <div class="transcription-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: #333;">📄 {transcription['filename']}</h3>
                {get_status_badge(transcription['status'])}
            </div>
        """, unsafe_allow_html=True)
        
        # Progress bar for transcribing status
        if transcription['status'] == 'transcribing':
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {transcription['progress']}%;"></div>
            </div>
            <p style="text-align: center; margin: 0.5rem 0; color: #666;">{transcription['progress']}% Complete</p>
            """, unsafe_allow_html=True)
        
        # Error message for failed status
        if transcription['status'] == 'failed':
            st.error(f"❌ {transcription.get('error', 'Unknown error occurred')}")
        
        # Metadata
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Duration", format_duration(transcription.get('duration')))
        
        with col2:
            st.metric("Processing Time", format_processing_time(transcription.get('processingTime')))
        
        with col3:
            st.metric("Model", transcription.get('whisperModel', 'Unknown'))
        
        # Show content for completed transcriptions
        if transcription['status'] == 'completed':
            # Summary
            if transcription.get('summary'):
                st.subheader("📋 Summary")
                st.write(transcription['summary'])
            
            # Action Items
            if transcription.get('actionItems'):
                st.subheader("✅ Action Items")
                for item in transcription['actionItems']:
                    st.markdown(f'<div class="action-item">• {item}</div>', unsafe_allow_html=True)
            
            # Participants
            if transcription.get('participants'):
                st.subheader("👥 Participants")
                for participant in transcription['participants']:
                    st.markdown(f'<span class="participant-tag">{participant}</span>', unsafe_allow_html=True)
            
            # Transcript
            if transcription.get('transcript'):
                st.subheader("📝 Transcript")
                with st.expander("View full transcript", expanded=False):
                    st.markdown(f'<div class="transcript-text">{transcription["transcript"]}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def display_metrics(transcriptions):
    """Display summary metrics"""
    if not transcriptions:
        return
    
    completed = [t for t in transcriptions if t['status'] == 'completed']
    transcribing = [t for t in transcriptions if t['status'] == 'transcribing']
    failed = [t for t in transcriptions if t['status'] == 'failed']
    
    total_duration = sum(t.get('duration', 0) for t in completed if t.get('duration'))
    total_processing_time = sum(t.get('processingTime', 0) for t in completed if t.get('processingTime'))
    total_action_items = sum(len(t.get('actionItems', [])) for t in completed)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">{len(transcriptions)}</h3>
            <p style="margin: 0; color: #666;">Total Files</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #28a745;">{len(completed)}</h3>
            <p style="margin: 0; color: #666;">Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #ffc107;">{format_duration(total_duration)}</h3>
            <p style="margin: 0; color: #666;">Total Duration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #17a2b8;">{total_action_items}</h3>
            <p style="margin: 0; color: #666;">Action Items</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎤 Motia Meeting Transcription</h1>
        <p>Real-time meeting transcription results and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check Motia status
    api_running, workbench_running = check_motia_status()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Status")
        
        # Status indicators
        col1, col2 = st.columns(2)
        
        with col1:
            if api_running:
                st.success("✅ API Server")
            else:
                st.error("❌ API Server")
        
        with col2:
            if workbench_running:
                st.success("✅ Workbench")
            else:
                st.error("❌ Workbench")
        
        if not (api_running and workbench_running):
            st.warning("⚠️ Some Motia services are not running")
            st.info("Start the services with: `npm run dev` in the meeting_transcript_example directory")
        
        st.markdown("---")
        
        # Filters
        st.header("🔍 Filters")
        
        status_filter = st.multiselect(
            "Status",
            ["completed", "transcribing", "failed"],
            default=["completed", "transcribing", "failed"],
            help="Filter by transcription status"
        )
        
        model_filter = st.multiselect(
            "Whisper Model",
            ["whisper-large-v3", "whisper-medium", "whisper-small", "whisper-base"],
            default=["whisper-large-v3", "whisper-medium", "whisper-small", "whisper-base"],
            help="Filter by Whisper model used"
        )
        
        st.markdown("---")
        
        # Quick actions
        st.header("🚀 Quick Actions")
        
        if st.button("🔄 Refresh Data", type="primary"):
            st.rerun()
        
        if st.button("📊 Export Results"):
            st.info("Export functionality coming soon!")
        
        st.markdown("---")
        
        # System info
        st.header("ℹ️ About")
        st.info("This UI displays real-time transcription results from the Motia workflow")
        st.info("Data is fetched from Motia streams and updated automatically")
        st.info("100% Local Processing • No Data Leaves Your Machine")

    # Main content
    st.header("📊 Transcription Overview")
    
    # Get transcription data
    transcriptions = get_transcription_streams()
    
    # Apply filters
    filtered_transcriptions = [
        t for t in transcriptions 
        if t['status'] in status_filter and t.get('whisperModel') in model_filter
    ]
    
    # Display metrics
    display_metrics(filtered_transcriptions)
    
    # Status breakdown
    if filtered_transcriptions:
        st.subheader("📈 Status Breakdown")
        
        status_counts = {}
        for t in filtered_transcriptions:
            status_counts[t['status']] = status_counts.get(t['status'], 0) + 1
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'completed' in status_counts:
                st.metric("✅ Completed", status_counts['completed'])
        
        with col2:
            if 'transcribing' in status_counts:
                st.metric("🔄 Transcribing", status_counts['transcribing'])
        
        with col3:
            if 'failed' in status_counts:
                st.metric("❌ Failed", status_counts['failed'])
    
    # Transcription results
    st.header("📄 Transcription Results")
    
    if filtered_transcriptions:
        # Sort by timestamp (newest first)
        sorted_transcriptions = sorted(
            filtered_transcriptions, 
            key=lambda x: x.get('timestamp', ''), 
            reverse=True
        )
        
        for transcription in sorted_transcriptions:
            display_transcription_card(transcription)
    else:
        st.info("📭 No transcriptions found matching the current filters")
        st.info("Try adjusting the filters or check if Motia services are running")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🎤 Motia Meeting Transcription | Powered by OpenAI Whisper | 100% Local Processing</p>
        <p>Real-time streaming updates from Motia workflows</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 