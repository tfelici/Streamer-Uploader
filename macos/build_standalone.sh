#!/bin/bash

# Streamer Uploader macOS Build Script
# Creates a standalone executable for macOS systems

echo "==========================================="
echo "  Streamer Uploader - macOS Build Script"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "../main.py" ]; then
    echo "❌ ERROR: main.py not found in parent directory"
    echo "   Please run this script from the macos/ directory"
    exit 1
fi

# Check if we're running on macOS
if [ "$(uname)" != "Darwin" ]; then
    echo "❌ ERROR: This script must be run on macOS"
    echo "   Current system: $(uname)"
    exit 1
fi

echo "✅ Running on macOS $(sw_vers -productVersion)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.7 or higher from python.org or using Homebrew:"
    echo "   brew install python"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $python_version"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ ERROR: pip3 is not installed or not in PATH"
    echo "   Please install pip3"
    exit 1
fi

echo "✅ pip3 is available"

# Check for Xcode Command Line Tools
if ! xcode-select -p &> /dev/null; then
    echo "❌ ERROR: Xcode Command Line Tools not installed"
    echo "   Please install with: xcode-select --install"
    exit 1
fi

echo "✅ Xcode Command Line Tools installed"

# Install/upgrade required packages
echo ""
echo "📦 Installing/upgrading required packages..."
pip3 install --upgrade pip
pip3 install -r ../requirements.txt
pip3 install pyinstaller

# Install macOS-specific dependencies for webview
echo ""
echo "📦 Installing macOS-specific dependencies..."
pip3 install pyobjc-framework-Cocoa pyobjc-framework-WebKit

# Check if PyInstaller is available
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ ERROR: PyInstaller installation failed"
    exit 1
fi

echo "✅ PyInstaller is available"

# Clean previous builds
echo ""
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -f *.spec~

# Build the executable
echo ""
echo "🔨 Building standalone executable..."
echo "   This may take a few minutes..."

pyinstaller StreamerUploader_onefile.spec

# Check if build was successful
if [ -f "dist/StreamerUploader" ]; then
    echo ""
    echo "✅ BUILD SUCCESSFUL!"
    echo ""
    echo "📁 Output location: macos/dist/StreamerUploader"
    
    # Get file size
    file_size=$(du -h dist/StreamerUploader | cut -f1)
    echo "📏 File size: $file_size"
    
    # Make executable
    chmod +x dist/StreamerUploader
    echo "✅ Executable permissions set"
    
    # Create data directory structure
    echo ""
    echo "📂 Creating data directory structure..."
    mkdir -p dist/streamerData/recordings/broadcast
    echo "✅ Directory structure created"
    
    # Optional: Code signing (commented out - requires developer certificate)
    # echo ""
    # echo "🔏 Code signing (optional)..."
    # codesign --force --deep --sign - dist/StreamerUploader
    
    echo ""
    echo "🎉 macOS build complete!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Copy the entire 'dist/' folder to your target macOS system"
    echo "   2. Run: ./StreamerUploader"
    echo "   3. Configure your upload server URL in Settings"
    echo ""
    echo "💡 The executable includes all dependencies and can run on"
    echo "   macOS systems without Python installation."
    echo ""
    echo "⚠️  Note: On first run, you may need to:"
    echo "   - Right-click → Open (instead of double-clicking)"
    echo "   - Allow in System Preferences → Security & Privacy"
    
else
    echo ""
    echo "❌ BUILD FAILED!"
    echo ""
    echo "🔍 Check the output above for error messages."
    echo "📋 Common issues:"
    echo "   - Missing Xcode Command Line Tools"
    echo "   - Python version incompatibility"
    echo "   - Missing Python packages (pyobjc)"
    echo ""
    echo "💡 Try installing missing dependencies:"
    echo "   pip3 install pyobjc-framework-Cocoa pyobjc-framework-WebKit"
    exit 1
fi
