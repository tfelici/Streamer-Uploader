# Encoder Uploader - Standalone Version

## SELF-CONTAINED EXECUTABLE - NO DEPENDENCIES REQUIRED

This is a completely self-contained version of the Encoder Uploader application that does not require Python, pip, or any external dependencies to run.

### What You Get:
- **Single executable file**: `EncoderUploader_Standalone.exe` (13.7 MB)
- **No Python required**: All dependencies are bundled inside the executable
- **No installation needed**: Just run the executable
- **Portable**: Copy the entire folder to any Windows machine and it will work

### Files Included:
```
EncoderUploader_Standalone/
├── EncoderUploader_Standalone.exe    (Main application - 13.7 MB)
└── encoderData/                      (Data directory)
    └── recordings/
        └── broadcast/                (Recording files go here)
```

### How to Use:
1. **Run the Application**: Double-click `EncoderUploader_Standalone.exe`
2. **No Setup Required**: The application will start immediately
3. **Data Storage**: All settings and recordings are stored in the `encoderData` folder

### Features:
- ✅ Integrated web browser viewer
- ✅ Upload recordings to remote servers
- ✅ Overlapping files detection
- ✅ Settings management
- ✅ All Flask templates and static files embedded
- ✅ No external dependencies

### Distribution:
- **For yourself**: Just run the executable from this folder
- **For others**: Copy the entire `EncoderUploader_Standalone` folder to any Windows machine
- **System Requirements**: Windows 7+ (32-bit or 64-bit)

### Comparison with Other Versions:
| Version | File Count | Size | Startup Speed | Portability |
|---------|------------|------|---------------|-------------|
| **Standalone** | 1 exe file | 13.7 MB | Slightly slower | ⭐⭐⭐⭐⭐ Maximum |
| **OneDirr** | Many files | ~15 MB total | Faster | ⭐⭐⭐ Good |

### Technical Details:
- Built with PyInstaller using `--onefile` mode
- All Python libraries bundled internally
- Templates and static files embedded
- UPX compression disabled for maximum compatibility
- No antivirus false positives (unsigned but clean)

### Troubleshooting:
- If Windows shows a security warning, click "More info" → "Run anyway" (this is normal for unsigned executables)
- If the app doesn't start, try running as administrator
- Check Windows Defender/antivirus isn't blocking the executable

**Built on:** June 3, 2025  
**Python Version:** 3.11.9  
**PyInstaller Version:** 6.13.0
