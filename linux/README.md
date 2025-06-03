# Linux Build Instructions

This directory contains the Linux build configuration for EncoderUploader.

## Prerequisites

- Python 3.7+
- pip package manager
- Linux environment (Ubuntu, CentOS, etc.)

## Build Process

1. **Navigate to linux directory**:
   ```bash
   cd linux/
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
   pyinstaller EncoderUploader_linux.spec
   ```

4. **Find executable**:
   - Output: `linux/dist/EncoderUploader`
   - Size: ~15-20MB (standalone)

## Files

- `EncoderUploader_linux.spec` - PyInstaller configuration
- `build_executable.sh` - Automated build script
- `dist/EncoderUploader` - Generated executable (after build)

## Features

✓ Standalone Linux executable  
✓ No external dependencies required  
✓ Real-time upload progress tracking  
✓ Integrated web viewer  
✓ Cross-platform compatibility  

## Download URL (when available)

```
https://github.com/tfelici/Encoder-Uploader/raw/main/linux/dist/EncoderUploader
```
