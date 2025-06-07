#!/bin/bash

# STT Typer Toggle Script
# Checks if the speech-to-text process is running and toggles it

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROCESS_NAME="main.py"
PID_FILE="/tmp/stt_typer.pid"

# Check if process is running
if pgrep -f "$PROCESS_NAME" > /dev/null; then
    echo "STT Typer is running. Stopping..."
    pkill -f "$PROCESS_NAME"
    rm -f "$PID_FILE"
    echo "STT Typer stopped."
else
    echo "STT Typer is not running. Starting..."
    cd "$SCRIPT_DIR"
    nohup uv run main.py > /tmp/stt_typer.log 2>&1 &
    echo $! > "$PID_FILE"
    echo "STT Typer started. PID: $(cat $PID_FILE)"
fi