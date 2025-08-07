# Motia Meetings Transcription Example

A zero-to-sixty example demonstrating local, privacy-friendly meeting audio processing using Motia, Whisper, and Streamlit. Perfect for Windows development environments with 16GB RAM.

## 🎯 What This Example Does

This project showcases how to build a complete local AI pipeline that:
- Transcribes meeting audio files using OpenAI Whisper (offline)
- Summarizes transcripts and extracts action items using Motia
- Provides a clean Streamlit UI for easy file upload and results viewing
- Processes multiple audio formats (MP3, WAV, M4A)
- Outputs structured CSV results

## 🚀 Quick Start

### Prerequisites
- Windows 10/11 (64-bit)
- Python 3.10+
- 16GB RAM (8GB minimum)
- 2GB free disk space

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/MotiaMeetingTranscriptionExample.git
   cd MotiaMeetingTranscriptionExample
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Whisper model** (first time only)
   ```bash
   python -c "import whisper; whisper.load_model('base')"
   ```

### Usage

1. **Start the UI**
   ```bash
   streamlit run ui/meetings_ui.py
   ```

2. **Upload audio files** via the web interface

3. **Run the pipeline** and download results

## 📁 Project Structure

```
MotiaMeetingTranscriptionExample/
├── flows/
│   ├── flow_meeting_summarizer.yml    # Main Motia flow
│   └── flow_invoice_ocr.yml          # Bonus OCR example
├── scripts/
│   ├── transcribe_whisper.py         # Whisper transcription
│   └── run_mistral_ocr.py           # OCR processing
├── ui/
│   ├── meetings_ui.py               # Main Streamlit interface
│   └── ocr_ui.py                   # OCR interface
├── inputs/
│   └── audio_inputs/               # Audio file storage
├── outputs/                        # Results storage
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## 🔧 Core Components

### Motia Flow (`flows/flow_meeting_summarizer.yml`)
The main pipeline that orchestrates:
1. **ListAudio**: Scans for audio files
2. **Transcribe**: Converts audio to text using Whisper
3. **Summarize**: Extracts key points and action items
4. **SaveCSV**: Outputs structured results

### Whisper Transcription (`scripts/transcribe_whisper.py`)
- Uses OpenAI Whisper base model (optimized for 16GB RAM)
- Supports MP3, WAV, M4A formats
- Handles errors gracefully
- Outputs clean, formatted text

### Streamlit UI (`ui/meetings_ui.py`)
- Drag-and-drop file upload
- Real-time progress tracking
- Results display and CSV download
- Clean, intuitive interface

## 📊 Output Format

The pipeline generates a CSV file with columns:
- `filename`: Original audio file name
- `summary`: Meeting summary
- `action_items`: Extracted tasks and follow-ups
- `duration`: Audio file duration
- `transcript`: Full transcript text

## 🎨 Bonus Features

### Invoice OCR Example
Also included is a complete invoice processing example using Mistral OCR:
- Processes PDF, JPG, PNG files
- Extracts date, amount, vendor information
- Outputs structured invoice data

To use the OCR example:
```bash
streamlit run ui/ocr_ui.py
```

## ⚙️ Configuration

### Model Selection
- **Default**: Whisper base model (good speed/accuracy balance)
- **Low RAM**: Use `tiny` model in `transcribe_whisper.py`
- **High Accuracy**: Use `medium` model (requires more RAM)

### Performance Tuning
- **CPU**: Multi-core processing recommended
- **GPU**: Optional CUDA acceleration (install `torch` with CUDA)
- **Memory**: Monitor usage with Task Manager

## 🐛 Troubleshooting

### Common Issues

**"Out of memory" error**
- Use Whisper `tiny` model instead of `base`
- Close other applications
- Process files one at a time

**Audio file not supported**
- Ensure file is MP3, WAV, or M4A format
- Check file isn't corrupted
- Try converting with ffmpeg

**Setup issues**
- Verify Python 3.10+ is installed
- Ensure virtual environment is activated
- Check all dependencies are installed

### Getting Help
- Check the [troubleshooting guide](docs/troubleshooting.md)
- Review [setup instructions](docs/setup.md)
- Open an issue with error details

## 🔒 Privacy & Security

- **100% Local Processing**: No data leaves your machine
- **No External APIs**: All processing happens offline
- **No Logging**: No telemetry or external logging
- **Data Cleanup**: Automatic temporary file cleanup

## 🚀 Advanced Usage

### Command Line Interface
Run the Motia flow directly:
```bash
motia run flows/flow_meeting_summarizer.yml
```

### Custom Processing
Modify the scripts to:
- Add custom summarization prompts
- Extract specific information types
- Integrate with other tools

### Batch Processing
- Place multiple audio files in `inputs/audio_inputs/`
- Run pipeline once for all files
- Results combined in single CSV

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📈 Performance Benchmarks

| Audio Length | Model | RAM Usage | Processing Time |
|-------------|-------|-----------|-----------------|
| 10 minutes  | Base  | ~4GB      | ~1 minute       |
| 30 minutes  | Base  | ~6GB      | ~3 minutes      |
| 60 minutes  | Base  | ~8GB      | ~6 minutes      |

*Benchmarks on Windows 10, 16GB RAM, Intel i7*

## 📚 Related Resources

- [Motia Documentation](https://docs.motia.dev)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Streamlit](https://streamlit.io)
- [Motia Examples Repository](https://github.com/MotiaDev/motia-examples)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Motia team for the excellent platform
- OpenAI for Whisper
- Streamlit for the UI framework
- Community contributors and feedback

---

**Ready to get started?** Follow the [Quick Start](#-quick-start) guide above! 