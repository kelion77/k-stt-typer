import logging
import os
import signal
import sys
import wave
import pyaudio
import threading
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

import pyautogui

api_key = os.getenv("GOOGLE_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
AUDIO_FILE = "/tmp/stt_recording.wav"

# Global variables for recording control
recording = False
record_thread = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global recording
    print("\nShutdown signal received. Stopping recording...")
    recording = False

def cleanup_audio_file():
    """Remove temporary audio file"""
    try:
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)
    except Exception as e:
        logger.error(f"Error cleaning up audio file: {e}")

def record_audio():
    """Record audio continuously until stopped"""
    global recording
    
    audio = pyaudio.PyAudio()
    
    try:
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=1024
        )
        
        frames = []
        print("Recording... Press Ctrl+C to stop.")
        
        while recording:
            data = stream.read(1024)
            frames.append(data)
        
        # Save recorded audio to file
        with wave.open(AUDIO_FILE, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        print(f"Audio saved to {AUDIO_FILE}")
        
    except Exception as e:
        logger.error(f"Error during recording: {e}")
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        audio.terminate()

def transcribe_audio():
    """Send audio file to Google Gemini for transcription"""
    try:
        if not os.path.exists(AUDIO_FILE):
            print("No audio file found to transcribe.")
            return
        
        client = genai.Client(api_key=api_key)
        
        print("Uploading audio file for transcription...")
        myfile = client.files.upload(file=AUDIO_FILE)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=["Generate a transcript of the speech. Do not include any other text. Output only in grammatically correct english. IF YOU HEAR ANYTHING ELSE THAN ENGLISH, TRANSLATE IT TO ENGLISH.", myfile]
        )
        
        if response.text:
            # Strip any trailing whitespace/newlines that might cause Enter to be pressed
            clean_text = response.text.strip()
            print(f"Transcription: {clean_text}")
            pyautogui.typewrite(clean_text)
        else:
            print("No transcription received.")
            
    except Exception as e:
        logger.error(f"Error during transcription: {e}")


def main():
    global recording, record_thread
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)
    
    # Clean up any existing audio file
    cleanup_audio_file()
    
    # Start recording
    recording = True
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()
    
    # Wait for user to stop recording (Ctrl+C will set recording to False)
    record_thread.join()
        
    # Transcribe the recorded audio
    if os.path.exists(AUDIO_FILE):
        transcribe_audio()
        
    cleanup_audio_file()


if __name__ == "__main__":
    main()
