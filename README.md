# Speech-to-Text Typer

A Python application that captures speech from your microphone and automatically types the transcribed text using AssemblyAI's real-time speech recognition.

## Features

- Real-time speech-to-text conversion
- Automatic typing of transcribed text
- Turn-based formatting for natural speech patterns
- Microphone audio stream processing
- Toggle script for easy start/stop control

## System Requirements

### Linux
Install these system packages before running the application:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-tk python3-dev alsa-utils pulseaudio-utils scrot xclip
```

**Fedora/RHEL:**
```bash
sudo dnf install tkinter python3-devel alsa-utils pulseaudio-utils scrot xclip
```

**Arch Linux:**
```bash
sudo pacman -S tk python alsa-utils pulseaudio scrot xclip
```

### macOS
Most dependencies are built-in. You may need:
```bash
# Install Xcode command line tools if not already installed
xcode-select --install
```

### General Requirements
- **Python**: 3.13 or higher
- **Microphone**: Working microphone with proper system permissions
- **Audio System**: ALSA/PulseAudio (Linux) or Core Audio (macOS)
- **Display Server**: X11 or Wayland (Linux) for GUI automation
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
   Edit `.env` and add your AssemblyAI API key:
   ```
   ASSEMBLYAI_API_KEY=your_actual_api_key_here
   ```

3. Get your API key from [AssemblyAI](https://www.assemblyai.com/)

## Usage

### Direct execution:
```bash
uv run main.py
```
Stop with `Ctrl+C`

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

The application connects to AssemblyAI's streaming API, captures audio from your microphone, and automatically types the transcribed text in real-time. It uses turn-based formatting to ensure natural speech patterns are maintained.

## Future Development

- Add configuration options for different audio sources
- Implement custom keyboard shortcuts for start/stop
- Add support for multiple languages
- Create GUI interface for easier control
- Add text formatting options (punctuation, capitalization)
- Implement hotword detection for activation
- Add support for custom vocabularies and domain-specific terms