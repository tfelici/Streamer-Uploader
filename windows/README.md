# Windows Standalone Executable Build

This directory contains the necessary files to build a standalone Windows executable for the Encoder Uploader application.

## Files Required for Building

### Essential Files:
- `EncoderUploader_onefile.spec` - PyInstaller specification file with optimized dependencies
- `build_standalone.bat` - Build script to create the standalone executable

### Build Process:
1. Run `build_standalone.bat`
2. The script will:
   - Install required Python packages
   - Clean previous builds
   - Create standalone executable using PyInstaller
   - Set up proper directory structure
   - Move executable to distribution folder

### Output:
- `dist\EncoderUploader_Standalone\EncoderUploader_Standalone.exe` - Main executable (13.7MB)
- `dist\EncoderUploader_Standalone\encoderData\` - Data directory structure
- `dist\EncoderUploader_Standalone\README.md` - Distribution documentation

## Features of Standalone Executable:
- ✅ Self-contained (no Python installation required)
- ✅ No external dependencies
- ✅ Integrated web browser viewer
- ✅ Recording upload functionality
- ✅ Settings management
- ✅ Overlapping files detection
- ✅ All Flask templates and static files bundled

## Distribution:
Copy the entire `EncoderUploader_Standalone` folder to target systems. The executable will work on any Windows machine without requiring Python or any other dependencies.

## File Size:
- Executable: ~13.7MB
- Total package: ~14MB (including directory structure)

## Build Requirements:
- Python 3.7+
- PyInstaller
- All packages from `../requirements.txt`

The build script handles all dependencies automatically.
