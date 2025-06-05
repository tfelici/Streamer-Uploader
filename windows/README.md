# Windows Standalone Executable Build

This directory contains the files needed to build a standalone Windows executable for the Streamer Uploader application.

## Quick Start

Run `build_standalone.bat` to create a single-file executable.

## Build Process

### Prerequisites
- Python 3.7+ installed and in PATH
- All dependencies will be installed automatically

### Build Steps
1. Run `build_standalone.bat`
2. The script will:
   - Install/upgrade required Python packages
   - Install/upgrade PyInstaller
   - Clean previous builds
   - Create standalone executable
   - Set up proper directory structure
   - Copy existing settings and recordings
   - Create ZIP distribution package

### Build Files
- **`build_standalone.bat`** - Main build script
- **`StreamerUploader_onefile.spec`** - PyInstaller specification with optimized dependencies
- **`version_info.txt`** - Windows executable version information

### Output Structure
```
dist/
├── StreamerUploader.exe (single standalone executable ~50MB)
└── encoderData/
    └── recordings/
        └── broadcast/
```

### Distribution
- **Single file**: `dist\StreamerUploader.exe`
- **ZIP package**: `StreamerUploader_Windows.zip` (ready for distribution)

## Features of Standalone Executable
- ✅ Self-contained single file (no Python installation required)
- ✅ No external dependencies
- ✅ Integrated web browser viewer (pywebview)
- ✅ Recording upload functionality with progress tracking
- ✅ Settings management
- ✅ Overlapping files detection
- ✅ Safe file removal for USB drives
- ✅ Video duration detection (pymediainfo)
- ✅ Cross-platform file operations
- ✅ Proper Windows executable metadata

## Usage
1. Extract or copy `StreamerUploader.exe` to desired location
2. Run the executable
3. Configure upload URL in settings
4. Upload recordings with progress tracking
- ✅ All Flask templates and static files bundled

## Distribution:
Copy the entire `StreamerUploader_Standalone` folder to target systems. The executable will work on any Windows machine without requiring Python or any other dependencies.

## File Size:
- Executable: ~13.7MB
- Total package: ~14MB (including directory structure)

## Build Requirements:
- Python 3.7+
- PyInstaller
- All packages from `../requirements.txt`

The build script handles all dependencies automatically.
