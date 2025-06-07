# Speech-to-Text Typer

A Python application that captures speech from your microphone and automatically types the transcribed text using AssemblyAI's real-time speech recognition.

## Features

- Real-time speech-to-text conversion
- Automatic typing of transcribed text
- Turn-based formatting for natural speech patterns
- Microphone audio stream processing

## Setup

1. Install dependencies:
   ```bash
   pip install assemblyai[extras] pyautogui
   ```

2. Create a `.env` file with your AssemblyAI API key:
   ```
   ASSEMBLYAI_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```bash
   python main.py
   ```

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