"""
Whisper.cpp integration module for speech-to-text transcription
Uses local whisper.cpp instead of cloud API for privacy and cost savings
"""

import logging
import os
import subprocess
import wave
import pyaudio
import threading
from pathlib import Path
from typing import Optional, Callable

logger = logging.getLogger(__name__)

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
AUDIO_FILE = "/tmp/stt_recording.wav"

# Whisper.cpp paths
WHISPER_CPP_DIR = Path(__file__).parent / "whisper.cpp"
WHISPER_CLI = WHISPER_CPP_DIR / "build" / "bin" / "whisper-cli"
WHISPER_STREAM = WHISPER_CPP_DIR / "build" / "bin" / "whisper-stream"
WHISPER_MODEL = WHISPER_CPP_DIR / "models" / "ggml-small.bin"
VAD_MODEL = WHISPER_CPP_DIR / "models" / "ggml-silero-v5.1.2.bin"


class WhisperRecorder:
    """Records audio and transcribes using whisper.cpp"""
    
    def __init__(self, language: str = "ko"):
        """
        Initialize recorder with whisper.cpp
        
        Args:
            language: Language code (default: 'ko' for Korean)
        """
        self.language = language
        self.recording = False
        self.record_thread = None
        
        # Validate whisper.cpp installation
        if not WHISPER_CLI.exists():
            raise FileNotFoundError(
                f"whisper-cli not found at {WHISPER_CLI}. "
                "Please build whisper.cpp first."
            )
        if not WHISPER_MODEL.exists():
            raise FileNotFoundError(
                f"Whisper model not found at {WHISPER_MODEL}. "
                "Please download the model first."
            )
    
    def start_recording(self):
        """Start recording audio in background thread"""
        if self.recording:
            logger.warning("Recording already in progress")
            return
        
        self.recording = True
        self.record_thread = threading.Thread(target=self._record_audio)
        self.record_thread.start()
        print("🎤 Recording... Press Ctrl+C to stop.")
    
    def stop_recording(self):
        """Stop recording audio"""
        if not self.recording:
            logger.warning("No recording in progress")
            return
        
        print("\n⏹️  Stopping recording...")
        self.recording = False
        if self.record_thread:
            self.record_thread.join()
        print(f"✅ Audio saved to {AUDIO_FILE}")
    
    def _record_audio(self):
        """Internal method to record audio continuously"""
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
            
            while self.recording:
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
            
            # Save recorded audio to file
            with wave.open(AUDIO_FILE, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
        except Exception as e:
            logger.error(f"Error during recording: {e}")
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            audio.terminate()
    
    def transcribe(self) -> Optional[str]:
        """
        Transcribe recorded audio using whisper.cpp
        
        Returns:
            Transcribed text or None if error
        """
        if not os.path.exists(AUDIO_FILE):
            logger.error("No audio file found to transcribe")
            return None
        
        try:
            print("🔄 Transcribing with whisper.cpp...")
            
            # Build whisper.cpp command
            cmd = [
                str(WHISPER_CLI),
                "-m", str(WHISPER_MODEL),
                "-f", AUDIO_FILE,
                "-l", self.language,
                "--output-txt",  # Output as text file
                "-of", "/tmp/stt_output",  # Output file prefix
                "--no-prints",  # Suppress verbose output
            ]
            
            # Add VAD if available
            if VAD_MODEL.exists():
                cmd.extend([
                    "--vad",
                    "-vm", str(VAD_MODEL)
                ])
            
            # Run whisper.cpp
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logger.error(f"Whisper transcription failed: {result.stderr}")
                return None
            
            # Read output file
            output_file = Path("/tmp/stt_output.txt")
            if output_file.exists():
                text = output_file.read_text().strip()
                output_file.unlink()  # Clean up
                print(f"✅ Transcription: {text}")
                return text
            else:
                logger.error("No output file generated")
                return None
            
        except subprocess.TimeoutExpired:
            logger.error("Transcription timeout")
            return None
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return None
    
    def cleanup(self):
        """Remove temporary audio file"""
        try:
            if os.path.exists(AUDIO_FILE):
                os.remove(AUDIO_FILE)
        except Exception as e:
            logger.error(f"Error cleaning up audio file: {e}")


class WhisperStreamer:
    """Real-time streaming transcription using whisper.cpp"""
    
    def __init__(self, language: str = "ko", on_text_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize streaming transcriber
        
        Args:
            language: Language code (default: 'ko' for Korean)
            on_text_callback: Callback function called with transcribed text
        
        Note:
            Streaming mode requires SDL2. Install with: brew install sdl2
            Then rebuild: cd whisper.cpp && cmake -B build -DWHISPER_SDL2=ON && cmake --build build
        """
        self.language = language
        self.on_text_callback = on_text_callback
        self.process = None
        
        # Validate whisper-stream binary (optional feature)
        if not WHISPER_STREAM.exists():
            raise FileNotFoundError(
                f"whisper-stream not found at {WHISPER_STREAM}.\n"
                "Streaming mode requires additional setup:\n"
                "  1. Install SDL2: brew install sdl2\n"
                "  2. Rebuild with SDL2: cd whisper.cpp && cmake -B build -DWHISPER_SDL2=ON && cmake --build build\n"
                "For basic usage, use WhisperRecorder instead."
            )
        if not WHISPER_MODEL.exists():
            raise FileNotFoundError(
                f"Whisper model not found at {WHISPER_MODEL}"
            )
    
    def start_streaming(self):
        """Start real-time streaming transcription"""
        print("🎤 Starting real-time transcription...")
        print("   Speak into your microphone. Press Ctrl+C to stop.")
        
        # Build whisper-stream command
        cmd = [
            str(WHISPER_STREAM),
            "-m", str(WHISPER_MODEL),
            "-l", self.language,
            "--step", "3000",  # Process every 3 seconds
            "--length", "8000",  # 8 second context
            "-t", "4",  # 4 threads
        ]
        
        # Add VAD if available
        if VAD_MODEL.exists():
            cmd.extend([
                "--vad",
                "-vm", str(VAD_MODEL)
            ])
        
        try:
            # Start streaming process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Read output line by line
            for line in self.process.stdout:
                line = line.strip()
                if line and self.on_text_callback:
                    # Filter out debug/status messages
                    if not line.startswith('[') and len(line) > 0:
                        self.on_text_callback(line)
            
        except KeyboardInterrupt:
            print("\n⏹️  Stopping stream...")
            self.stop_streaming()
        except Exception as e:
            logger.error(f"Error during streaming: {e}")
            self.stop_streaming()
    
    def stop_streaming(self):
        """Stop streaming transcription"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
        print("✅ Streaming stopped")

