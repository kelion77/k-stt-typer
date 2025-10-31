#!/bin/bash

# Install Hammerspoon for reliable global hotkeys
# Hammerspoon is free and the best tool for macOS hotkeys

echo "=================================================="
echo "🎯 Setting up WORKING global hotkey"
echo "=================================================="
echo ""
echo "Installing Hammerspoon (the ONLY reliable way)..."
echo ""

# Install Hammerspoon via Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found"
    echo "Please install Homebrew first: https://brew.sh"
    exit 1
fi

echo "📦 Installing Hammerspoon..."
brew install --cask hammerspoon

# Wait for installation
sleep 2

# Create Hammerspoon config
mkdir -p ~/.hammerspoon

# Get absolute path to project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat > ~/.hammerspoon/init.lua << EOF
-- STT Typer Hotkey Configuration
-- Simple toggle - Python handles the paste

-- Hide menu bar icon
hs.menuIcon(false)

-- Primary hotkey: Ctrl + Alt + Space
hs.hotkey.bind({"ctrl", "alt"}, "space", function()
    -- Just run the toggle script, Python will handle everything
    hs.task.new("/bin/bash", nil, {"${PROJECT_DIR}/toggle_whisper.sh"}):start()
end)

-- Secondary hotkey: Shift + Cmd + , (comma)
hs.hotkey.bind({"shift", "cmd"}, ",", function()
    -- Same toggle script
    hs.task.new("/bin/bash", nil, {"${PROJECT_DIR}/toggle_whisper.sh"}):start()
end)
EOF

echo ""
echo "✅ Hammerspoon installed and configured!"
echo ""
echo "=================================================="
echo "📋 Next steps:"
echo "=================================================="
echo ""
echo "1. Hammerspoon will open automatically"
echo "2. Click 'Open' if prompted"
echo "3. Allow Accessibility permissions when asked"
echo "4. Look for Hammerspoon icon in menu bar (🔨)"
echo "5. Press hotkey anywhere to use STT!"
echo ""
echo "Done! Your hotkeys are configured:"
echo "  - Primary: ⌃⌥Space (Control+Option+Space)"
echo "  - Secondary: ⇧⌘, (Shift+Command+Comma)"
echo ""

