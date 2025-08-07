#!/usr/bin/env python3
"""
Report Generation Script for Motia Meeting Transcription Example

This script generates HTML reports from CSV results for better visualization
and sharing of meeting transcription results.
"""

import sys
import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

def generate_html_report(csv_file: str, output_file: str) -> str:
    """
    Generate an HTML report from CSV results
    
    Args:
        csv_file: Path to input CSV file
        output_file: Path to output HTML file
        
    Returns:
        Path to generated HTML file
    """
    
    # Read CSV data
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    # Generate HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meeting Transcription Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .meeting-item {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 5px;
        }}
        .meeting-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .meeting-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .meeting-duration {{
            background-color: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        .meeting-summary {{
            margin-bottom: 15px;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
            border: 1px solid #e9ecef;
        }}
        .action-items {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
        }}
        .action-items h4 {{
            color: #856404;
            margin-top: 0;
        }}
        .transcript-preview {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin-top: 15px;
            max-height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        .timestamp {{
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            .summary-stats {{
                grid-template-columns: 1fr;
            }}
            .meeting-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Meeting Transcription Report</h1>
        
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-number">{len(df)}</div>
                <div class="stat-label">Meetings Processed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['duration'].sum():.1f}</div>
                <div class="stat-label">Total Duration (minutes)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['transcript'].str.len().sum()}</div>
                <div class="stat-label">Total Characters</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['action_items'].notna().sum()}</div>
                <div class="stat-label">Meetings with Action Items</div>
            </div>
        </div>
        
        <h2>📝 Meeting Details</h2>
"""
    
    # Add each meeting
    for index, row in df.iterrows():
        filename = row.get('filename', f'Meeting {index + 1}')
        summary = row.get('summary', 'No summary available')
        action_items = row.get('action_items', 'No action items identified')
        duration = row.get('duration', 0)
        transcript = row.get('transcript', 'No transcript available')
        
        # Format duration
        duration_str = f"{duration:.1f} min" if duration > 0 else "Unknown"
        
        # Truncate transcript for preview
        transcript_preview = transcript[:500] + "..." if len(transcript) > 500 else transcript
        
        html_content += f"""
        <div class="meeting-item">
            <div class="meeting-header">
                <div class="meeting-title">🎤 {filename}</div>
                <div class="meeting-duration">⏱️ {duration_str}</div>
            </div>
            
            <div class="meeting-summary">
                <h4>📋 Summary</h4>
                <p>{summary}</p>
            </div>
            
            <div class="action-items">
                <h4>✅ Action Items</h4>
                <p>{action_items}</p>
            </div>
            
            <div class="transcript-preview">
                <h4>📄 Transcript Preview</h4>
                <p>{transcript_preview}</p>
            </div>
        </div>
"""
    
    # Add footer
    html_content += f"""
        <div class="timestamp">
            Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </div>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return None

def main():
    """Main entry point for the script"""
    if len(sys.argv) != 3:
        print("Usage: python generate_report.py <csv_file> <output_html_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Validate input file
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    # Generate report
    result = generate_html_report(csv_file, output_file)
    
    if result:
        print(f"Report generation successful: {result}")
        sys.exit(0)
    else:
        print("Report generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 