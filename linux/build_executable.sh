#!/bin/bash
# Linux build script for EncoderUploader

echo "Building EncoderUploader for Linux..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Check if required packages are installed
echo "Installing required packages..."
pip install -r ../requirements.txt

# Build the executable
echo "Building executable..."
pyinstaller EncoderUploader_linux.spec

# Check if build was successful
if [ -f "dist/EncoderUploader" ]; then
    echo "✓ Build successful!"
    echo "Executable created: linux/dist/EncoderUploader"
    echo "File size: $(du -h dist/EncoderUploader | cut -f1)"
else
    echo "✗ Build failed!"
    exit 1
fi

echo "Build complete!"
