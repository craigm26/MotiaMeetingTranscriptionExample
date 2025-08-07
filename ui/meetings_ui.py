#!/usr/bin/env python3
"""
Streamlit UI for Motia Meeting Transcription Example

This provides a user-friendly interface for uploading audio files,
running the transcription pipeline, and viewing results.
"""

import streamlit as st
import subprocess
import os
import pandas as pd
import time
from pathlib import Path
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Motia Meeting Transcription",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .file-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-message {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_onedrive_recordings_path():
    """Get the OneDrive Teams recordings path for the current user"""
    username = os.getenv('USERNAME', os.getenv('USER', 'CraigM'))
    onedrive_paths = [
        f"C:\\Users\\{username}\\OneDrive - NCPA\\Recordings",
        f"C:\\Users\\{username}\\OneDrive\\Recordings", 
        f"C:\\Users\\{username}\\OneDrive - Personal\\Recordings",
        f"C:\\Users\\{username}\\OneDrive - Company\\Recordings"
    ]
    
    for path in onedrive_paths:
        if Path(path).exists():
            return path
    
    # Fallback to default if none found
    return f"C:\\Users\\{username}\\OneDrive - NCPA\\Recordings"

def create_directories():
    """Create necessary directories"""
    directories = [
        "inputs/audio_inputs",
        "outputs",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def get_teams_recordings():
    """Get list of Teams recordings from OneDrive"""
    recordings_path = get_onedrive_recordings_path()
    recordings = []
    
    if Path(recordings_path).exists():
        # Look for MP4 files (Teams recordings)
        for file_path in Path(recordings_path).rglob("*.mp4"):
            recordings.append({
                'name': file_path.name,
                'path': str(file_path),
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                'relative_path': file_path.relative_to(Path(recordings_path))
            })
    
    return recordings, recordings_path

def copy_file_to_inputs(source_path, filename):
    """Copy file from OneDrive to inputs directory"""
    import shutil
    dest_path = Path("inputs/audio_inputs") / filename
    
    try:
        shutil.copy2(source_path, dest_path)
        return str(dest_path)
    except Exception as e:
        st.error(f"Error copying file: {e}")
        return None

def save_uploaded_files(uploaded_files):
    """Save uploaded files to inputs directory"""
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = Path("inputs/audio_inputs") / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(str(file_path))
    return saved_files

def run_motia_pipeline():
    """Run the Motia pipeline"""
    try:
        result = subprocess.run(
            ["python", "scripts/transcribe_whisper.py"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def load_results():
    """Load results from outputs directory"""
    results = {}
    
    csv_path = Path("outputs/meeting_summaries.csv")
    if csv_path.exists():
        try:
            results['csv'] = pd.read_csv(csv_path)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    
    html_path = Path("outputs/meeting_report.html")
    if html_path.exists():
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                results['html'] = f.read()
        except Exception as e:
            st.error(f"Error reading HTML: {e}")
    
    return results

def display_metrics(df):
    """Display summary metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Meetings Processed", len(df))
    
    with col2:
        total_duration = df['duration'].sum() if 'duration' in df.columns else 0
        st.metric("Total Duration (min)", f"{total_duration:.1f}")
    
    with col3:
        total_chars = df['transcript'].str.len().sum() if 'transcript' in df.columns else 0
        st.metric("Total Characters", f"{total_chars:,}")
    
    with col4:
        action_items = df['action_items'].notna().sum() if 'action_items' in df.columns else 0
        st.metric("Meetings with Action Items", action_items)

def main():
    st.markdown("""<div class="main-header">
        <h1>🎤 Motia Meeting Transcription</h1>
        <p>Transcribe and summarize Microsoft Teams recordings from OneDrive</p>
    </div>""", unsafe_allow_html=True)
    
    create_directories()

    with st.sidebar:
        st.header("⚙️ Settings")
        model_size = st.selectbox("Whisper Model Size", ["base", "tiny", "small", "medium", "large"])
        batch_processing = st.checkbox("Enable batch processing", value=True)
        generate_report = st.checkbox("Generate HTML report", value=True)
        
        st.subheader("ℹ️ System Info")
        st.info(f"Model: Whisper {model_size}")
        st.info("Platform: Local Processing")
        st.info("Privacy: 100% Offline")
        
        # Show OneDrive path
        recordings_path = get_onedrive_recordings_path()
        st.subheader("📁 OneDrive Path")
        st.info(f"Recordings: {recordings_path}")
        
        if not Path(recordings_path).exists():
            st.warning("⚠️ OneDrive recordings path not found")

    # Teams Recordings Section
    st.header("📹 Microsoft Teams Recordings")
    
    recordings, recordings_path = get_teams_recordings()
    
    if recordings:
        st.success(f"📁 Found {len(recordings)} Teams recordings in OneDrive")
        
        # Display recordings in a nice format
        for recording in recordings:
            with st.expander(f"🎥 {recording['name']}", expanded=False):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**Path:** `{recording['relative_path']}`")
                    st.write(f"**Size:** {recording['size'] / (1024*1024):.1f} MB")
                    st.write(f"**Modified:** {recording['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                with col2:
                    if st.button(f"▶️ Process", key=f"process_{recording['name']}"):
                        with st.spinner(f"Processing {recording['name']}..."):
                            # Copy file to inputs
                            copied_path = copy_file_to_inputs(recording['path'], recording['name'])
                            if copied_path:
                                # Run transcription
                                success, stdout, stderr = run_motia_pipeline()
                                if success:
                                    st.success(f"✅ {recording['name']} processed successfully!")
                                    st.session_state.processing_complete = True
                                else:
                                    st.error(f"❌ Processing failed: {stderr}")
                
                with col3:
                    if st.button(f"📋 View Details", key=f"details_{recording['name']}"):
                        st.json({
                            "name": recording['name'],
                            "full_path": recording['path'],
                            "size_bytes": recording['size'],
                            "modified": recording['modified'].isoformat()
                        })
        
        # Batch processing option
        if batch_processing and len(recordings) > 1:
            st.markdown("---")
            if st.button("🚀 Process All Recordings", type="primary"):
                with st.spinner("Processing all recordings..."):
                    processed_count = 0
                    for recording in recordings:
                        copied_path = copy_file_to_inputs(recording['path'], recording['name'])
                        if copied_path:
                            success, stdout, stderr = run_motia_pipeline()
                            if success:
                                processed_count += 1
                    
                    if processed_count > 0:
                        st.success(f"✅ Successfully processed {processed_count}/{len(recordings)} recordings!")
                        st.session_state.processing_complete = True
                    else:
                        st.error("❌ No recordings were processed successfully")
    
    else:
        st.info(f"📁 No Teams recordings found in: {recordings_path}")
        st.info("Teams recordings are typically saved as .mp4 files in your OneDrive Recordings folder")

    # Manual Upload Section
    st.header("📁 Manual File Upload")
    st.info("Upload audio files manually if they're not in your OneDrive Recordings folder")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_files = st.file_uploader(
            "Choose audio files",
            type=['mp3', 'wav', 'm4a', 'flac', 'ogg', 'mp4'],
            accept_multiple_files=True,
            help="Upload audio files for transcription"
        )
        
        if uploaded_files:
            st.success(f"📎 {len(uploaded_files)} file(s) selected.")
            
            # Show file details
            file_details = []
            for file in uploaded_files:
                file_details.append({
                    "Name": file.name,
                    "Size": f"{file.size / (1024*1024):.1f} MB",
                    "Type": file.type
                })
            st.dataframe(pd.DataFrame(file_details))

    with col2:
        st.header("🚀 Process")
        if uploaded_files:
            if st.button("🎯 Start Transcription", type="primary"):
                with st.spinner("Processing files..."):
                    saved_files = save_uploaded_files(uploaded_files)
                    success, stdout, stderr = run_motia_pipeline()
                    if success:
                        st.success("✅ Processing completed successfully!")
                        st.session_state.processing_complete = True
                    else:
                        st.error("❌ Processing failed")
                        st.error(f"Error: {stderr}")
                        with st.expander("Debug Information"):
                            st.text("STDOUT:")
                            st.code(stdout)
                            st.text("STDERR:")
                            st.code(stderr)
        else:
            st.info("📁 Please upload audio files to begin")

    # Results Section
    if st.session_state.get('processing_complete', False) or Path("outputs/meeting_summaries.csv").exists():
        st.header("📊 Results")
        results = load_results()
        
        if 'csv' in results:
            df = results['csv']
            display_metrics(df)
            
            st.subheader("📋 Meeting Summaries")
            st.dataframe(df, use_container_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="meeting_summaries.csv",
                    mime="text/csv"
                )
            
            with col2:
                if 'html' in results:
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=results['html'],
                        file_name="meeting_report.html",
                        mime="text/html"
                    )
            
            # HTML Report Preview
            if 'html' in results:
                st.subheader("📄 HTML Report Preview")
                st.components.v1.html(results['html'], height=600, scrolling=True)
            
            # Individual Meeting Details
            st.subheader("🔍 Meeting Details")
            if len(df) > 0:
                selected_meeting = st.selectbox(
                    "Select a meeting to view details:",
                    df['filename'].tolist() if 'filename' in df.columns else df.index.tolist()
                )
                
                if selected_meeting:
                    meeting_data = df[df['filename'] == selected_meeting] if 'filename' in df.columns else df.iloc[selected_meeting:selected_meeting+1]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📝 Summary")
                        st.write(meeting_data['summary'].iloc[0] if 'summary' in meeting_data.columns else "No summary available")
                    
                    with col2:
                        st.subheader("✅ Action Items")
                        action_items = meeting_data['action_items'].iloc[0] if 'action_items' in meeting_data.columns else "No action items"
                        st.write(action_items)

    st.markdown("---")
    st.markdown("""<div style="text-align: center;">
        <p>🎤 Motia Meeting Transcription | Powered by OpenAI Whisper | 100% Local Processing</p>
        <p>Automatically detects Microsoft Teams recordings from OneDrive</p>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 