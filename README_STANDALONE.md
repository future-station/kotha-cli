# Kotha CLI - Standalone Version

Convert video files to MP3 and transcribe them to text using Google's Gemini AI.

## 📦 What's Included

- `kotha.exe` - Standalone executable (no Python required!)
- `install_standalone.bat` - Automatic installer
- `README_STANDALONE.md` - This file

## 🚀 Quick Start

### Option 1: Automatic Installation (Recommended)

1. Run `install_standalone.bat` as administrator
2. Follow the on-screen instructions
3. Restart your command prompt
4. Use `kotha` from anywhere!

### Option 2: Manual Setup

1. Copy `kotha.exe` to a folder (e.g., `C:\kotha-cli\`)
2. Add that folder to your Windows PATH
3. Use `kotha` from anywhere!

## ⚙️ Setup

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy your API key

### 2. Set Your API Key

```cmd
kotha --set-api="your-gemini-api-key-here"
```

## 📖 Usage

### Process all videos in current directory

```cmd
kotha
```

### Process a specific video

```cmd
kotha video.mp4
```

### Get help

```cmd
kotha --help
```

### Check version

```cmd
kotha --version
```

## 📁 Output

The tool creates:

- `audio/` folder with MP3 files
- `text/` folder with transcribed text

## 🎯 Supported Formats

- **Video**: MP4, MKV, AVI, MOV, WebM
- **Languages**: Bengali, English, and many others

## ❓ Troubleshooting

### "kotha is not recognized as a command"

- Make sure you ran the installer or added kotha.exe to your PATH
- Restart your command prompt

### "GEMINI_API_KEY not found"

- Set your API key: `kotha --set-api="your-key"`

### Antivirus warnings

- The executable is safe - it's just a packaged Python application
- You may need to add an exception for kotha.exe

## 📊 System Requirements

- Windows 10/11 (64-bit)
- ~100MB disk space
- Internet connection for transcription

## 🔒 Privacy

- Your API key is stored locally in `%USERPROFILE%\.kotha\config.json`
- Video files are processed locally
- Only audio is sent to Google's Gemini API for transcription

---

Made with ❤️ by akr4m | Version 1.0.0
