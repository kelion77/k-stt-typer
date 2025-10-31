#!/bin/bash

# Installation script for whisper.cpp integration
# This script sets up whisper.cpp for local speech-to-text

set -e

echo "=================================================="
echo "🚀 Installing whisper.cpp for STT Typer"
echo "=================================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is optimized for macOS"
    echo "   For other platforms, manual installation may be required"
fi

# Install CMake if needed (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v cmake &> /dev/null; then
        echo "📦 Installing CMake via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install cmake
        else
            echo "❌ Homebrew not found. Please install CMake manually."
            exit 1
        fi
    else
        echo "✅ CMake already installed"
    fi
fi

# Clone whisper.cpp if not exists
if [ ! -d "whisper.cpp" ]; then
    echo "📥 Cloning whisper.cpp repository..."
    git clone https://github.com/ggml-org/whisper.cpp.git
else
    echo "✅ whisper.cpp directory already exists"
fi

# Build whisper.cpp
echo "🔨 Building whisper.cpp..."
cd whisper.cpp
make
cd ..

# Download models
echo "📥 Downloading Whisper base model (141MB)..."
cd whisper.cpp
bash ./models/download-ggml-model.sh base

echo "📥 Downloading VAD model (864KB)..."
bash ./models/download-vad-model.sh silero-v5.1.2
cd ..

echo ""
echo "=================================================="
echo "✅ Installation complete!"
echo "=================================================="
echo ""
echo "📋 Next steps:"
echo "   1. Test basic recording: uv run main_whisper.py"
echo "   2. Try real-time mode: uv run stream_whisper.py"
echo "   3. Use toggle script: ./toggle_whisper.sh"
echo ""
echo "💡 Tips:"
echo "   - Basic mode: Record → Ctrl+C → Transcribe → Type"
echo "   - Stream mode: Speaks → Transcribes → Types in real-time"
echo "   - Works offline (no internet required)"
echo "   - Free (no API costs)"
echo ""


