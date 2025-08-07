# Local Meeting Transcription System

A Motia-powered local meeting transcription system that monitors and processes audio files using local Whisper API. This system tracks all local activity in the repository and provides real-time transcription with analysis.

## 🎯 Project Goal

The primary goal is to create a **local meeting transcription system** that:
- Uses local Whisper API for transcription
- Monitors all local activity in the repository
- Provides real-time transcription with analysis
- Tracks system health and local API status

## 🏗️ Architecture

### Core Components

1. **Meeting Transcription API** (`/transcribe-meeting`)
   - Accepts audio file requests
   - Integrates with local Whisper API
   - Provides real-time streaming updates

2. **Local Whisper Integration**
   - Uses local Whisper models
   - Processes audio files locally
   - Tracks processing time and model status

3. **Real-time Streaming**
   - Live updates during transcription
   - Local system monitoring
   - Error handling and status tracking

4. **Local Activity Monitoring**
   - Tracks repository file changes
   - Monitors local API health
   - Provides system status updates

### Steps Overview

- **`12-meeting-transcription-api.step.ts`** - API endpoint for transcription requests
- **`13-meeting-transcription-processor.step.ts`** - Processes transcription with local Whisper
- **`meeting-transcription.stream.ts`** - Real-time streaming for transcription updates

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.8+ (for local Whisper API)
- Local Whisper installation

### Installation

```bash
cd meeting_transcript_example
npm install
```

### Running the System

```bash
# Generate types
npm run generate-types

# Start the Motia server
npm start
```

### API Usage

#### Start Transcription

```bash
curl -X POST http://localhost:3000/transcribe-meeting \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "meeting_audio.wav",
    "language": "en",
    "model": "whisper-large-v3",
    "localWhisperPath": "./scripts/transcribe_whisper.py"
  }'
```

#### Check Local Status

```bash
curl http://localhost:3000/local-status
```

## 📁 Project Structure

```
meeting_transcript_example/
├── steps/
│   ├── 12-meeting-transcription-api.step.ts      # API endpoint
│   ├── 13-meeting-transcription-processor.step.ts # Local Whisper processor
│   ├── meeting-transcription.stream.ts           # Real-time streaming
│   └── hello-world.step.js                       # Basic API test
├── flows/
│   └── flow_meeting_transcription.yml            # Main transcription flow
├── scripts/
│   └── transcribe_whisper.py                     # Local Whisper integration
└── inputs/
    └── audio_inputs/                             # Audio files directory
```

## 🔧 Local Whisper Integration

The system integrates with local Whisper API through:

1. **Local Model Loading** - Uses local Whisper models
2. **Audio Processing** - Processes audio files locally
3. **Real-time Updates** - Provides streaming updates during processing
4. **Error Handling** - Handles local API failures gracefully

### Whisper Models Supported

- `whisper-1` - Base model
- `whisper-large-v3` - Large model (default)

## 📊 Real-time Streaming

The system provides real-time updates through Motia streams:

### Meeting Transcription Stream

```typescript
{
  status: 'uploading' | 'transcribing' | 'processing' | 'completed' | 'failed',
  progress: number,
  filename: string,
  localWhisperStatus: string,
  whisperModel: string,
  processingTime: number,
  transcript?: string,
  participants?: string[],
  actionItems?: string[]
}
```

### System Monitoring Stream

```typescript
{
  type: 'error' | 'cleanup' | 'health' | 'maintenance' | 'local-activity',
  status: 'info' | 'warning' | 'error' | 'success',
  localApiStatus: string,
  whisperModelStatus: string,
  message: string
}
```

## 🧪 Testing

### Test the API

```bash
# Test basic connectivity
curl http://localhost:3000/hello-world

# Test transcription endpoint
curl -X POST http://localhost:3000/transcribe-meeting \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.wav"}'
```

## 🔍 Monitoring

The system monitors:

- **Local Whisper API status**
- **Processing times**
- **Model loading status**
- **Repository activity**
- **System health**

## 🛠️ Development

### Adding New Steps

1. Create step file in `steps/` directory
2. Define config and handler
3. Update flow in `flows/flow_meeting_transcription.yml`
4. Run `npm run generate-types`

### Local Development

```bash
# Watch for changes
npm run dev

# Generate types after changes
npm run generate-types
```

## 📝 Notes

- This system focuses **only** on local meeting transcription
- All processing happens locally using Whisper API
- Real-time streaming provides live updates
- System monitors local repository activity
- No external API dependencies for transcription

## 🤝 Contributing

1. Focus on local Whisper integration
2. Maintain local processing capabilities
3. Add local monitoring features
4. Test with local audio files

---

**Focus**: Local meeting transcription with Whisper API integration and repository activity monitoring. 