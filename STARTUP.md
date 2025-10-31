# Startup Guide After Reboot

**[한국어 문서](STARTUP.ko.md)**

## Current Status

- Hammerspoon menubar icon hidden
- Hotkey `⌃⌥Space` always works

---

## After Reboot

### Method 1: Hammerspoon Auto-Start (Recommended)

**One-time setup!**

1. **Open Hammerspoon**
   ```bash
   open -a Hammerspoon
   ```

2. **Click Hammerspoon icon in menubar** (appears temporarily)

3. **Check "Launch Hammerspoon at login"**

4. **Done!** Now auto-starts after reboot
   - Menubar icon stays hidden (already configured)
   - `⌃⌥Space` hotkey works immediately

---

### Method 2: Manual Start

If Hammerspoon is not running after reboot:

```bash
open -a Hammerspoon
```

Or search "Hammerspoon" in Spotlight (`⌘Space`) and launch

---

## Understanding Microphone Indicator

### Current Behavior:

1. **Normally**: Hammerspoon icon hidden
2. **Press ⌃⌥Space**:
   - macOS detects microphone usage
   - **Orange microphone indicator appears in Control Center**
3. **Stop recording**: Microphone indicator disappears

### Orange Microphone Indicator:

```
Control Center (top right) → 🎤 Orange dot
```

This is:
- **Normal behavior!**
- macOS security feature (shows app is using microphone)
- Only appears while recording
- **Cannot be hidden** (for security)

---

## Full Automation Setup

### 1. Hammerspoon Auto-Start on Login

```bash
# Launch Hammerspoon
open -a Hammerspoon

# Click menubar icon → Preferences → "Launch Hammerspoon at login" check
```

### 2. Verify

After reboot:
```bash
# Check if Hammerspoon is running
ps aux | grep Hammerspoon | grep -v grep
```

If running → Auto-start success!
If nothing shown → Manually run `open -a Hammerspoon`

---

## Quick Checklist

After reboot:

1. [ ] Hammerspoon running?
   - Check: `ps aux | grep Hammerspoon | grep -v grep`
   - If not: `open -a Hammerspoon`

2. [ ] Hammerspoon icon hidden in menubar? (normal)

3. [ ] `⌃⌥Space` works?
   - Test in Notes app
   - If not: Restart Hammerspoon

---

## Expected Behavior

### Normal State:
```
Normally:
- Menubar: Clean (no icon)
- Hotkey: Works

While recording:
- Menubar: 🎤 Orange microphone indicator (macOS system)
- Hotkey: Press ⌃⌥Space to stop

After recording:
- Menubar: Clean (microphone indicator disappears)
- Text: Auto-typed
```

---

## Troubleshooting

### Orange microphone icon stays on (Most Common!)

**Symptom**: Control Center shows orange microphone even after stopping recording

**Cause**: `main_whisper.py` process still running in background

**Immediate Solution**:
```bash
# Run emergency stop script
cd k-stt-typer  # or your project directory
./stop_all.sh
```

**Manual Solution**:
```bash
# 1. Check running processes
ps aux | grep main_whisper

# 2. Force kill all
pkill -9 -f main_whisper.py

# 3. Clean PID files
rm -f /tmp/stt_whisper.pid /tmp/stt_whisper.status
```

**Prevention**: Latest `toggle_whisper.sh` prevents this automatically

---

### Hammerspoon icon keeps showing:

```bash
# 1. Check configuration
cat ~/.hammerspoon/init.lua | grep menuIcon
# → Should have hs.menuIcon(false)

# 2. Restart Hammerspoon
killall Hammerspoon
open -a Hammerspoon

# 3. Verify icon is gone
```

### Hotkey not working:

```bash
# Check if Hammerspoon is running
ps aux | grep Hammerspoon

# If not running, launch it
open -a Hammerspoon

# Check logs
tail -f /tmp/stt_whisper_toggle_debug.log
```

### Microphone permission error:

```
System Settings → Privacy & Security → Microphone
→ Python / Terminal check
```

---

## Tips

### Check auto-start:

```bash
# Check login items
osascript -e 'tell application "System Events" to get the name of every login item'
```

If "Hammerspoon" appears, auto-start is configured!

### Complete Hammerspoon restart:

```bash
killall Hammerspoon && sleep 1 && open -a Hammerspoon
```

---

## Summary

### One-time Setup:
1. `hs.menuIcon(false)` configured (already done)
2. Hammerspoon → "Launch at login" check

### After Reboot:
- Hammerspoon auto-starts (if configured)
- Icon stays hidden
- `⌃⌥Space` ready to use
- 🎤 indicator only while recording (macOS system)

---

## Complete!

Now you have:
- Hammerspoon icon hidden
- 🎤 Microphone indicator only while recording (normal)
- Auto-start after reboot (if configured)

**The orange microphone indicator is a macOS security feature - this is normal!**
