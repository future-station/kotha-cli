# Kotha CLI 🎥➡️📝

A powerful command-line tool that converts video files to MP3 and transcribes them to text using Google's Gemini AI.

## Features

- 🎬 **Video to Audio Conversion**: Supports multiple formats (MP4, MKV, AVI, MOV, WebM)
- 🤖 **AI-Powered Transcription**: Uses Google's Gemini 2.0 Flash model for accurate transcription
- 🌍 **Multi-language Support**: Supports transcription in multiple languages including Bengali
- 💾 **Persistent API Key Storage**: Set your API key once and use from anywhere
- 📁 **Organized Output**: Automatically creates `audio/` and `text/` directories
- 🚀 **Fast & Efficient**: Progress bars and optimized processing

## Installation

### Quick Install (Windows)

1. **Download and run the installer:**
   - Download `install.bat` from the releases
   - Right-click and "Run as administrator" (optional, but recommended)
   - Follow the on-screen instructions

### Manual Installation

#### Option 1: Install from PyPI (Recommended)

```bash
pip install kotha-cli
```

#### Option 2: Install from Source

```bash
git clone <repository-url>
cd kotha_cli
pip install .
```

#### Option 3: Using the Python installer

```bash
# Download install.py and run:
python install.py
```

## Setup

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy your API key

### 2. Set Your API Key

```bash
kotha --set-api="your-gemini-api-key-here"
```

This will save your API key securely on your machine, and you won't need to set it again.

## Usage

### Basic Usage

Convert and transcribe all video files in the current directory:

```bash
kotha
```

### Process a Specific File

```bash
kotha video_file.mp4
```

### Set/Update API Key

```bash
kotha --set-api="your-new-api-key"
```

### Get Version

```bash
kotha --version
```

## How It Works

1. **🔍 Detection**: Finds all video files in the current directory
2. **🎵 Conversion**: Converts videos to MP3 format (stored in `audio/` directory)
3. **📝 Transcription**: Sends audio to Gemini AI for transcription
4. **💾 Storage**: Saves transcribed text to `text/` directory

## Supported Video Formats

- MP4 (`.mp4`)
- MKV (`.mkv`)
- AVI (`.avi`)
- MOV (`.mov`)
- WebM (`.webm`)

## Output Structure

```
your-directory/
├── video1.mp4
├── video2.mp4
├── audio/
│   ├── video1.mp3
│   └── video2.mp3
└── text/
    ├── video1.txt
    └── video2.txt
```

## Configuration

Your API key is stored in:

- **Windows**: `C:\Users\{username}\.kotha\config.json`
- **macOS**: `/Users/{username}/.kotha/config.json`
- **Linux**: `/home/{username}/.kotha/config.json`

## Requirements

- Python 3.8+
- FFmpeg (automatically installed with moviepy)
- Google Gemini API key

## Troubleshooting

### "GEMINI_API_KEY not found"

Make sure you've set your API key:

```bash
kotha --set-api="your-api-key"
```

### Video conversion issues

Ensure FFmpeg is properly installed. It should be automatically installed with moviepy, but if you encounter issues:

**Windows**:

```bash
# Install via chocolatey
choco install ffmpeg
```

**macOS**:

```bash
# Install via homebrew
brew install ffmpeg
```

**Linux**:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note**: This tool requires a Google Gemini API key. Usage of the Gemini API may incur costs based on Google's pricing structure.
