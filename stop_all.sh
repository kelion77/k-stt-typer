#!/bin/bash

# Emergency stop script
# Use this if the microphone icon won't go away

echo "🛑 Stopping all STT processes..."

# Kill all main_whisper.py processes
pkill -9 -f "main_whisper.py" 2>/dev/null

# Clean up PID and status files
rm -f /tmp/stt_whisper.pid
rm -f /tmp/stt_whisper.status

# Verify all processes are gone
if pgrep -f "main_whisper.py" > /dev/null 2>&1; then
    echo "❌ Some processes still running. Try manually:"
    echo "   ps aux | grep main_whisper"
    echo "   kill -9 <PID>"
else
    echo "✅ All processes stopped!"
    echo "✅ Microphone icon should disappear now"
fi

