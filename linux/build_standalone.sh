#!/bin/bash

# Streamer Uploader Linux Build Script
# Creates a standalone executable for Linux systems

echo "==========================================="
echo "  Streamer Uploader - Linux Build Script"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "../main.py" ]; then
    echo "❌ ERROR: main.py not found in parent directory"
    echo "   Please run this script from the linux/ directory"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.7 or higher"
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

# Install/upgrade required packages
echo ""
echo "📦 Installing/upgrading required packages..."
pip3 install --upgrade pip
pip3 install -r ../requirements.txt
pip3 install pyinstaller

# Check if PyInstaller is available
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ ERROR: PyInstaller installation failed"
    exit 1
fi

echo "✅ PyInstaller is available"

# Install Linux-specific dependencies for webview
echo ""
echo "📦 Installing Linux-specific dependencies..."
echo "   Note: You may need to install system packages manually:"
echo "   Ubuntu/Debian: sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0"
echo "   CentOS/RHEL: sudo yum install python3-gobject gtk3-devel webkit2gtk3-devel"

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
    echo "📁 Output location: linux/dist/StreamerUploader"
    
    # Get file size
    file_size=$(du -h dist/StreamerUploader | cut -f1)
    echo "📏 File size: $file_size"
    
    # Make executable
    chmod +x dist/StreamerUploader
    echo "✅ Executable permissions set"
    
    # Create data directory structure
    echo ""
    echo "📂 Creating data directory structure..."
    mkdir -p dist/encoderData/recordings/broadcast
    echo "✅ Directory structure created"
    
    echo ""
    echo "🎉 Linux build complete!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Copy the entire 'dist/' folder to your target Linux system"
    echo "   2. Run: ./StreamerUploader"
    echo "   3. Configure your upload server URL in Settings"
    echo ""
    echo "💡 The executable includes all dependencies and can run on"
    echo "   Linux systems without Python installation."
    
else
    echo ""
    echo "❌ BUILD FAILED!"
    echo ""
    echo "🔍 Check the output above for error messages."
    echo "📋 Common issues:"
    echo "   - Missing system packages (GTK, WebKit)"
    echo "   - Python version incompatibility"
    echo "   - Missing Python packages"
    echo ""
    echo "💡 For Ubuntu/Debian, try:"
    echo "   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0"
    exit 1
fi
