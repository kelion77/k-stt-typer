#!/bin/bash

# Improved toggle script with better state management
# Works reliably with keyboard shortcuts

PIDFILE="/tmp/stt_whisper.pid"
LOGFILE="/tmp/stt_whisper.log"
STATUSFILE="/tmp/stt_whisper.status"
DEBUG_LOG="/tmp/stt_whisper_toggle_debug.log"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure predictable PATH (Shortcuts / Automator have limited env)
export PATH="$HOME/.local/bin:$HOME/miniforge3/bin:$HOME/anaconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Locate uv binary (try common locations)
UV_BIN=""
for path in "$HOME/.local/bin/uv" "$HOME/miniforge3/bin/uv" "$HOME/anaconda3/bin/uv" "/opt/homebrew/bin/uv" "/usr/local/bin/uv"; do
    if [ -x "$path" ]; then
        UV_BIN="$path"
        break
    fi
done

# If not found in common locations, try PATH
if [ -z "$UV_BIN" ]; then
    UV_BIN="$(command -v uv 2>/dev/null)"
fi

# Logging helper
log_debug() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$DEBUG_LOG"
}

# Function to show notification
notify() {
    osascript -e "display notification \"$1\" with title \"STT Typer\" sound name \"Ping\"" 2>/dev/null || true
}

log_debug "Toggle invoked"

if [ -z "$UV_BIN" ]; then
    msg="uv binary not found. Please ensure uv is installed."
    log_debug "$msg"
    notify "$msg"
    exit 1
fi

log_debug "Using uv at $UV_BIN"

# Kill all existing main_whisper.py processes (safety check)
# Prevent duplicate processes
cleanup_all_processes() {
    pkill -f "main_whisper.py" 2>/dev/null
    rm -f "$PIDFILE" "$STATUSFILE"
    log_debug "Cleaned up all main_whisper.py processes"
}

# Check if recording
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        # Recording is active, stop it
        echo "⏹️  Stopping recording..."
        log_debug "Stopping PID $PID"
        kill -SIGINT "$PID" 2>/dev/null
        
        # Wait for transcription to complete
        sleep 1
        
        # Clean up everything (including any orphaned processes)
        cleanup_all_processes
        
        echo "✅ Stopped"
        log_debug "Recording stopped successfully"
    else
        # Stale PID file - clean up everything
        echo "⚠️  Cleaning up stale processes"
        log_debug "Stale PID file detected"
        cleanup_all_processes
    fi
else
    # Check if any main_whisper.py is already running (shouldn't happen, but safety check)
    if pgrep -f "main_whisper.py" > /dev/null 2>&1; then
        echo "⚠️  Found existing processes. Cleaning up..."
        log_debug "Found orphaned main_whisper.py processes"
        cleanup_all_processes
        sleep 0.5
    fi
    
    # Not recording, start it
    echo "🎤 Starting recording..."
    log_debug "Starting new recording session"
    
    cd "$SCRIPT_DIR" || {
        log_debug "Failed to cd to $SCRIPT_DIR"
        exit 1
    }
    
    # Start recording in background
    nohup "$UV_BIN" run main_whisper.py > "$LOGFILE" 2>&1 &
    PID=$!

    # Give process moment to start
    sleep 0.5
    if ! kill -0 "$PID" 2>/dev/null; then
        log_debug "Failed to start process. See $LOGFILE"
        exit 1
    fi
    
    echo "$PID" > "$PIDFILE"
    echo "recording" > "$STATUSFILE"
    
    echo "✅ Started (PID: $PID)"
    log_debug "Recording started with PID $PID"
fi


