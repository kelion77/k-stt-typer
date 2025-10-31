# STT Typer - Whisper.cpp

**One hotkey** speech-to-text tool for Mac - supports 99+ languages

> This project is based on [vertuzz/stt-typer](https://github.com/vertuzz/stt-typer) and [whisper.cpp](https://github.com/ggml-org/whisper.cpp).

**[한국어 문서](README.ko.md)**

## Features

- **Dual hotkeys**: `⌃⌥Space` or `⇧⌘,` - choose what feels natural
- **Completely free**: Local whisper.cpp execution, no API costs
- **Privacy-first**: All processing done locally, no internet required
- **Multilingual**: Supports Korean, English, and other languages via Whisper
- **GPU acceleration**: Apple Silicon (M1/M2/M3/M4) Metal auto-enabled
- **Auto-paste**: Automatically types at cursor position

## Quick Start

### Prerequisites

Before installation, ensure you have:

1. **Homebrew** installed ([https://brew.sh](https://brew.sh))
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **PortAudio** library (required for PyAudio)
   ```bash
   brew install portaudio
   ```

3. **uv** package manager (will auto-install if missing)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Installation

```bash
# Clone repository
git clone https://github.com/kelion77/k-stt-typer.git
cd k-stt-typer

# Install Python dependencies (uv will auto-install if missing)
# If you see "command not found: uv", run: $HOME/.local/bin/uv sync
uv sync

# Install Whisper.cpp + models
./install_whisper.sh

# Install Hammerspoon (hotkey manager)
./setup_global_hotkey.sh
```

### Permission Setup

#### 1. Accessibility Permission (Required)
When running Hammerspoon, grant **Accessibility** permission:
- System Settings → Privacy & Security → Accessibility
- Find and enable **Hammerspoon**
- You may need to click the lock icon to make changes

#### 2. Microphone Permission (Required)
For audio recording, grant **Microphone** permission:
- System Settings → Privacy & Security → Microphone
- Find and enable **Python** or **Terminal** (depending on how you run it)
- If you see gibberish transcriptions like "is a is is", check this permission first

#### 3. Launch Hammerspoon
After installation, Hammerspoon should launch automatically. If not:
```bash
open -a Hammerspoon
```
Look for the Hammerspoon icon (🔨) in your menu bar.

### Usage

```
1. In any app (VS Code, Notes, Chrome, etc.)
2. Press ⌃⌥Space or ⇧⌘, once → Recording starts
3. Speak in Korean (e.g., "안녕하세요")
4. Press the same hotkey again → Auto-typed!
```

**Available hotkeys:**
- `⌃⌥Space` (Control + Option + Space) - Primary hotkey
- `⇧⌘,` (Shift + Command + Comma) - Secondary hotkey

## How It Works

```
⌃⌥Space (Hammerspoon)
  ↓
toggle_whisper.sh
  ↓
main_whisper.py (recording)
  ↓
⌃⌥Space (stop)
  ↓
Whisper.cpp (transcription)
  ↓
pynput (Cmd+V auto-paste)
  ↓
Typed at cursor!
```

## Key Files

```
k-stt-typer/
├── main_whisper.py           # Main app (record + transcribe + paste)
├── whisper_transcriber.py    # Whisper.cpp integration module
├── toggle_whisper.sh         # Toggle script
├── install_whisper.sh        # Whisper.cpp installer
├── setup_global_hotkey.sh    # Hammerspoon installer
└── whisper.cpp/              # Whisper.cpp (local STT)
    ├── models/
    │   ├── ggml-base.bin           # Whisper model (141MB)
    │   └── ggml-silero-v5.1.2.bin  # VAD model
    └── build/bin/whisper-cli       # CLI tool
```

## Usage Examples

### Writing comments in VS Code
```
1. Place cursor at comment position
2. ⌃⌥Space
3. "This function handles user authentication"
4. ⌃⌥Space
→ // This function handles user authentication
```

### Long sentences in Notes
```
1. ⌃⌥Space
2. "Today's tasks are writing project documentation, attending team meeting, and completing code review"
3. ⌃⌥Space
→ Full sentence auto-typed!
```

## Changing Hotkey

The default hotkey is `⌃⌥Space` (Control + Option + Space). To change it:

1. **Open Hammerspoon configuration**:
   ```bash
   open ~/.hammerspoon/init.lua
   ```

2. **Edit the hotkey binding** (line ~8):
   ```lua
   -- Current: Ctrl + Alt + Space
   hs.hotkey.bind({"ctrl", "alt"}, "space", function()

   -- Examples:
   -- Ctrl + Alt + . (period)
   hs.hotkey.bind({"ctrl", "alt"}, ".", function()

   -- Cmd + Shift + Space
   hs.hotkey.bind({"cmd", "shift"}, "space", function()

   -- F13 key (no modifiers)
   hs.hotkey.bind({}, "f13", function()
   ```

3. **Reload Hammerspoon**:
   ```bash
   killall Hammerspoon && open -a Hammerspoon
   ```

### Available Modifier Keys
- `cmd` - Command (⌘)
- `ctrl` - Control (⌃)
- `alt` - Option (⌥)
- `shift` - Shift (⇧)
- Combine multiple: `{"cmd", "shift", "ctrl"}`

### Available Keys
- Letters: `"a"`, `"b"`, `"c"`, etc.
- Function keys: `"f1"`, `"f2"`, ..., `"f20"`
- Special: `"space"`, `"return"`, `"escape"`, `"tab"`
- See [Hammerspoon key codes](https://www.hammerspoon.org/docs/hs.hotkey.html) for full list

## Language Configuration

The language is configured in [main_whisper.py:70](main_whisper.py#L70).

### Current Setting: Korean
```python
recorder = WhisperRecorder(language="ko")
```

### Changing Language

Edit [main_whisper.py](main_whisper.py):

```python
# For English only
recorder = WhisperRecorder(language="en")

# For auto-detection (recommended for multilingual use)
recorder = WhisperRecorder(language="auto")

# For Japanese
recorder = WhisperRecorder(language="ja")

# For Chinese
recorder = WhisperRecorder(language="zh")
```

### Important Notes

1. **Language-locked mode** (`language="ko"`):
   - Whisper will ALWAYS try to transcribe in Korean
   - English speech → Korean phonetic transcription (incorrect)
   - Fast and accurate for single language use

2. **Auto-detection mode** (`language="auto"`):
   - Whisper detects the spoken language automatically
   - Works for multilingual users
   - Slightly slower than language-locked mode

3. **Translation is NOT supported**:
   - Whisper transcribes speech in the SAME language
   - Speaking Korean → Korean text only
   - Speaking English → English text only
   - Cannot convert Korean speech to English text

### Supported Languages

Whisper supports 99+ languages including:
- Korean (ko), English (en), Japanese (ja), Chinese (zh)
- Spanish (es), French (fr), German (de), Russian (ru)
- And many more...

See [whisper.cpp language codes](https://github.com/ggml-org/whisper.cpp) for full list.

## Troubleshooting

### Gibberish or incorrect transcriptions (e.g., "is a is is is")

If you get nonsensical results instead of your speech:

1. **Check Microphone Permission** (most common issue)
   - System Settings → Privacy & Security → Microphone
   - Enable **Python** or **Terminal**
   - Restart the app after granting permission

2. **Test microphone is working**
   - Try recording in Voice Memos app
   - Check input level in System Settings → Sound → Input

3. **Check logs for errors**
   ```bash
   tail -f /tmp/stt_whisper.log
   ```

### Installation Issues

#### `command not found: uv`
The uv package manager was not found in PATH. Use the full path:
```bash
$HOME/.local/bin/uv sync
```

Or add it to your PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### `fatal error: 'portaudio.h' file not found`
PyAudio build failed due to missing PortAudio library:
```bash
brew install portaudio
uv sync  # Retry installation
```

### Performance Issues (Intel Macs)

**Note**: This tool works best on Apple Silicon Macs (M1/M2/M3/M4) with Metal GPU acceleration.

If you're on an **Intel Mac** and experiencing slow transcription:
- CPU-only processing is slower (no Metal GPU support)
- Consider using the `base` model instead of `small` for faster processing
- Transcription may take 5-10 seconds instead of 1-2 seconds

To switch to base model:
```bash
# 1. Download base model
cd whisper.cpp
bash ./models/download-ggml-model.sh base

# 2. Edit whisper_transcriber.py line 27
# Change: WHISPER_MODEL = WHISPER_CPP_DIR / "models" / "ggml-base.bin"
```

### Microphone icon stays on

If the orange microphone icon doesn't disappear after stopping:

```bash
# Run emergency stop script
./stop_all.sh
```

**Cause**: Duplicate processes or improper termination
**Solution**: The script cleans up all processes and removes the microphone icon

Manual check:
```bash
# Check running processes
ps aux | grep main_whisper

# Manual termination
pkill -9 -f main_whisper.py
rm -f /tmp/stt_whisper.pid
```

### Auto-paste not working
→ System Settings → Privacy & Security → Accessibility
→ Enable **Hammerspoon**

### Low transcription accuracy
→ Speak close to microphone in quiet environment
→ Check microphone permission (see above)
→ Or use larger model (small, medium)

### Hammerspoon not launching
```bash
# Launch manually
open -a Hammerspoon

# Check if installed
ls -la /Applications/Hammerspoon.app
```

### View logs
```bash
# Main log
tail -f /tmp/stt_whisper.log

# Toggle debug log
tail -f /tmp/stt_whisper_toggle_debug.log
```

## Model Comparison

| Model | Size | Speed | Accuracy | Recommendation |
|-------|------|-------|----------|----------------|
| base | 141MB | Fast | Good | When speed matters |
| **small** | **466MB** | **Medium** | **Excellent** | **Currently in use** |
| medium | 1.5GB | Slow | Best | Maximum accuracy |

### Changing Models

To switch to a different model:
```bash
# 1. Download model
cd whisper.cpp
bash ./models/download-ggml-model.sh medium  # or base, large

# 2. Edit whisper_transcriber.py
# WHISPER_MODEL = WHISPER_CPP_DIR / "models" / "ggml-medium.bin"
```

## Core Technologies

1. **Whisper.cpp** - C++ port of OpenAI Whisper
   - Metal GPU acceleration (M1/M2/M3/M4 auto-detection)
   - 3-4x faster than CPU-only
2. **Hammerspoon** - macOS automation, global hotkeys
3. **pynput** - Python keyboard control, auto-paste
4. **VAD (Voice Activity Detection)** - Automatic voice detection

## GPU Acceleration Check

Check in execution logs:
```bash
tail -f /tmp/stt_whisper.log | grep -i "gpu\|metal"
```

If GPU is successfully in use:
```
use gpu    = 1
GPU name:   Apple M3 Max
ggml_metal_device_init: ...
```

## License

MIT License

## Credits and References

### Based On
- [**vertuzz/stt-typer**](https://github.com/vertuzz/stt-typer) - Original project (Google Gemini API based)
- [**whisper.cpp**](https://github.com/ggml-org/whisper.cpp) - C++ port of OpenAI Whisper (local execution)

### Tools Used
- [Hammerspoon](https://www.hammerspoon.org/) - macOS automation and global hotkeys
- [pynput](https://pypi.org/project/pynput/) - Python keyboard control
