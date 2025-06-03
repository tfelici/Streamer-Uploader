# macOS Build Instructions

This directory contains the macOS build configuration for EncoderUploader.

## Prerequisites

- Python 3.7+
- pip package manager
- macOS environment
- Xcode Command Line Tools (for some dependencies)

## Build Process

1. **Navigate to macos directory**:
   ```bash
   cd macos/
   ```

2. **Make build script executable**:
   ```bash
   chmod +x build_executable.sh
   ```

3. **Run build script**:
   ```bash
   ./build_executable.sh
   ```

   Or manually:
   ```bash
   pip install -r ../requirements.txt
   pyinstaller EncoderUploader_macos.spec
   ```

4. **Find executable**:
   - Output: `macos/dist/EncoderUploader`
   - Size: ~15-20MB (standalone)

## Files

- `EncoderUploader_macos.spec` - PyInstaller configuration
- `build_executable.sh` - Automated build script
- `dist/EncoderUploader` - Generated executable (after build)

## Features

✓ Native macOS executable  
✓ No external dependencies required  
✓ Real-time upload progress tracking  
✓ Integrated web viewer  
✓ Cross-platform compatibility  

## Download URL (when available)

```
https://github.com/tfelici/Encoder-Uploader/raw/main/macos/dist/EncoderUploader
```
