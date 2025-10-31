"""
Main application using whisper.cpp for speech-to-text
This version uses local whisper.cpp instead of cloud API
- No internet required
- No API costs
- Better privacy
- Works with Korean and other languages
"""

import logging
import signal
import sys
import subprocess
from whisper_transcriber import WhisperRecorder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global recorder instance
recorder = None


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global recorder
    print("\n🛑 Shutdown signal received...")
    if recorder:
        recorder.stop_recording()
        # Transcribe and type the recorded audio
        text = recorder.transcribe()
        if text:
            print(f"⌨️  Typing: {text}")
            print(f"📋 Text: {text}")
            
            # Copy to clipboard
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            print("✅ Copied to clipboard")
            
            # Use pynput to paste directly
            import time
            time.sleep(0.3)
            
            try:
                from pynput.keyboard import Controller, Key
                keyboard = Controller()
                # Press Cmd+V
                keyboard.press(Key.cmd)
                keyboard.press('v')
                keyboard.release('v')
                keyboard.release(Key.cmd)
                print("✅ Pasted!")
            except Exception as e:
                print(f"❌ Paste failed: {e}")
                print("💡 Please press Cmd+V manually")
        recorder.cleanup()
    sys.exit(0)


def main():
    """Main application entry point"""
    global recorder
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize recorder with Korean language
        recorder = WhisperRecorder(language="ko")
        
        print("=" * 60)
        print("🎙️  STT Typer - Whisper.cpp Edition")
        print("=" * 60)
        print("✅ Using local whisper.cpp (no internet required)")
        print("✅ Korean language support")
        print("✅ VAD (Voice Activity Detection) enabled")
        print("-" * 60)
        
        # Start recording
        recorder.start_recording()
        
        # Wait for user to stop recording (Ctrl+C will trigger signal handler)
        while True:
            signal.pause()
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\n📋 Setup instructions:")
        print("   1. Make sure whisper.cpp is installed in ./whisper.cpp/")
        print("   2. Build whisper.cpp: cd whisper.cpp && make")
        print("   3. Download model: bash ./models/download-ggml-model.sh base")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


