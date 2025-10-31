#!/bin/bash

# Quick script to switch between models

MODEL=$1

if [ -z "$MODEL" ]; then
    echo "Usage: ./switch_model.sh [base|small|medium]"
    echo ""
    echo "Current model:"
    grep "WHISPER_MODEL" whisper_transcriber.py | grep -v "^#"
    exit 1
fi

MODEL_FILE="ggml-${MODEL}.bin"
MODEL_PATH="whisper.cpp/models/$MODEL_FILE"

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Model not found: $MODEL_PATH"
    echo ""
    echo "Download it first:"
    echo "  cd whisper.cpp"
    echo "  bash ./models/download-ggml-model.sh $MODEL"
    exit 1
fi

# Update whisper_transcriber.py
sed -i.bak "s|WHISPER_MODEL = WHISPER_CPP_DIR / \"models\" / \"ggml-.*\.bin\"|WHISPER_MODEL = WHISPER_CPP_DIR / \"models\" / \"$MODEL_FILE\"|" whisper_transcriber.py

echo "✅ Switched to $MODEL model!"
echo ""
grep "WHISPER_MODEL" whisper_transcriber.py | grep -v "^#"

