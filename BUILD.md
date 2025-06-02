# Encoder Uploader - Build Instructions

## Quick Build (Windows)

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Build executable**: `cd windows && build_executable.bat`

## Essential Files

- **`main.py`** - Main application code
- **`requirements.txt`** - Dependencies
- **`windows/EncoderUploader.spec`** - Windows build configuration
- **`windows/build_executable.bat`** - Windows build script
- **`templates/index.html`** - Web interface
- **`static/style.css`** - Styling
- **`encoderData/`** - Data directory (settings & recordings)

## Output

- **`windows/dist/EncoderUploader.exe`** - Standalone executable (13.8 MB)
- Ready to distribute as a single file

## Platform-Specific Builds

### Windows
- Navigate to `windows/` folder
- Run `build_executable.bat`
- Output: `windows/dist/EncoderUploader.exe`

### Linux (Future)
- Files will be in `linux/` folder
- Build scripts to be created

### macOS (Future)  
- Files will be in `macos/` folder
- Build scripts to be created

## Features

? Standalone Windows executable  
? Integrated web viewer (no browser needed)  
? Upload recordings to server  
? Delete local recordings  
? Overlapping files detection with timeline  
? Automatic port detection (5000-5009)  
? Settings management  

Ready for production use!
