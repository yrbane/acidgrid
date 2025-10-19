#!/bin/bash
# ACIDGRID Ableton Live Remote Script Installer
# Automatically installs ACIDGRID Remote Script to Ableton

set -e

echo "🎹 ACIDGRID Ableton Live Installer"
echo "==================================="
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    REMOTE_SCRIPTS_DIR="$HOME/Music/Ableton/User Library/Remote Scripts"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    REMOTE_SCRIPTS_DIR="$HOME/.local/share/Ableton/User Library/Remote Scripts"
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "Please install manually. See INSTALL.md"
    exit 1
fi

echo "✓ Detected OS: $OS"
echo "✓ Remote Scripts directory: $REMOTE_SCRIPTS_DIR"
echo ""

# Check if acidgrid package is installed
echo "Checking ACIDGRID Python package..."
if ! python3 -c "import acidgrid" 2>/dev/null; then
    echo "❌ ACIDGRID package not found!"
    echo ""
    echo "Please install it first:"
    echo "  pip install -e ."
    echo ""
    exit 1
fi
echo "✓ ACIDGRID package installed"
echo ""

# Create Remote Scripts directory if it doesn't exist
if [ ! -d "$REMOTE_SCRIPTS_DIR" ]; then
    echo "Creating Remote Scripts directory..."
    mkdir -p "$REMOTE_SCRIPTS_DIR"
    echo "✓ Directory created"
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="$SCRIPT_DIR/ACIDGRID"
TARGET_DIR="$REMOTE_SCRIPTS_DIR/ACIDGRID"

# Check if ACIDGRID folder already exists
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  ACIDGRID Remote Script already exists"
    read -p "Overwrite? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 1
    fi
    rm -rf "$TARGET_DIR"
fi

# Copy files
echo "Installing ACIDGRID Remote Script..."
cp -r "$SOURCE_DIR" "$TARGET_DIR"

# Verify installation
if [ -f "$TARGET_DIR/__init__.py" ] && \
   [ -f "$TARGET_DIR/ACIDGRID.py" ] && \
   [ -f "$TARGET_DIR/ClipCreator.py" ] && \
   [ -f "$TARGET_DIR/config.py" ]; then
    echo "✓ Files copied successfully"
else
    echo "❌ Installation failed - files missing"
    exit 1
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Open Ableton Live"
echo "2. Open Preferences (Cmd+,)"
echo "3. Go to Link/Tempo/MIDI tab"
echo "4. Select 'ACIDGRID' in Control Surface dropdown"
echo "5. Set Input/Output to 'None' (or your MIDI controller)"
echo "6. Restart Ableton Live"
echo ""
echo "Check Log.txt for '[ACIDGRID] Remote Script loaded!' message"
echo ""
echo "🎵 Happy generating!"
