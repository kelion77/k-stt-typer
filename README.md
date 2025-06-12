# Speech-to-Text Typer

A Python application that captures speech from your microphone and automatically types the transcribed text using Google Gemini API.

## Features

- Record audio from microphone with manual control (Ctrl+C to stop)
- Transcribe recorded audio using Google Gemini API
- Automatic typing of transcribed text
- Multi-language support with automatic translation to English
- Toggle script for easy start/stop control
- Background operation with logging

## System Requirements

### Linux
Install these system packages before running the application:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-dev portaudio19-dev xclip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-devel portaudio-devel xclip
```

**Arch Linux:**
```bash
sudo pacman -S python portaudio xclip
```

### macOS
Most dependencies are built-in. You may need:
```bash
# Install Xcode command line tools if not already installed
xcode-select --install
# Install portaudio if needed
brew install portaudio
```

### General Requirements
- **Python**: 3.13 or higher
- **Microphone**: Working microphone with proper system permissions
- **Audio System**: PortAudio for microphone input
- **Display Server**: GUI automation capabilities (built-in for most systems)
- **Permissions**: Microphone and accessibility permissions may be required

## Setup

1. Install dependencies using uv:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. Get your API key from [Google AI Studio](https://aistudio.google.com/)

## Usage

### Direct execution:
```bash
uv run main.py
```
Recording will start immediately. Stop recording with `Ctrl+C` to transcribe and type the audio.

### Toggle script (recommended):
```bash
./toggle_stt.sh
```
- First run: starts the application in background
- Second run: stops the application
- Logs are saved to `/tmp/stt_typer.log`

### System-wide access:
```bash
sudo ln -s $(pwd)/toggle_stt.sh /usr/local/bin/toggle-stt
toggle-stt
```

### Keyboard shortcut:
Add to Lubuntu keyboard shortcuts:
- Command: `/full/path/to/your/project/toggle_stt.sh`  
- Key combination: your choice (e.g., `Super+S`)

## How it works

The application records audio from your microphone until you stop it with Ctrl+C. It then uploads the audio file to Google Gemini API for transcription and automatically types the transcribed text. The system supports multiple languages and automatically translates non-English speech to English.
