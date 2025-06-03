# Encoder Uploader - Standalone Windows Application

A standalone application that replicates the "Upload Recordings" functionality from the RPI Encoder app, packaged as a Windows executable with integrated web viewer.

## Features

- **Standalone Windows Executable**: No Python installation required for end users
- **Integrated Web Viewer**: Native window with built-in browser (no external browser needed)
- **Upload Recordings**: Upload MP4 recordings to configured server
- **Delete Recordings**: Remove recordings from local storage
- **Settings Management**: Configure upload server URL
- **Overlapping Files Detection**: Visual timeline showing file overlaps on server
- **Modern UI**: Responsive design with progress bars and status indicators

## Quick Start

### For End Users (Download Ready-to-Use Executable)

**Option 1: Direct Download from Git Repository**
1. **Download**: The standalone executable is included in this repository at:
   `windows/dist/EncoderUploader_Standalone/EncoderUploader_Standalone.exe` (13.7MB)
2. **Download the entire folder**: `windows/dist/EncoderUploader_Standalone/`
3. **Run**: Double-click `EncoderUploader_Standalone.exe` (no installation required)
4. **Configure**: Set your upload server URL in Settings
5. **Use**: Upload or delete recordings as needed

**Features of the Standalone Executable:**
- ✅ **No Dependencies**: No Python or other software installation required
- ✅ **Self-Contained**: All libraries and dependencies bundled (13.7MB)
- ✅ **Native Window**: Integrated web browser viewer
- ✅ **Portable**: Copy to any Windows machine and run immediately

### For Developers (Building from Source)

#### Prerequisites

- Python 3.7 or higher
- Windows 10 or higher

#### Building the Executable

1. **Clone/Download** this repository
2. **Install Dependencies**:
   ```bat
   pip install -r requirements.txt
   ```
3. **Build Executable**:
   ```bat
   cd windows
   build_standalone.bat
   ```
4. **Find Output**: The executable will be in `windows/dist/EncoderUploader_Standalone/`

#### Testing Before Building

To test the integrated viewer before building:
```bat
python main.py
```

## File Structure

```
Encoder Uploader/
├── main.py                    # Main application with integrated viewer
├── requirements.txt           # Python dependencies
├── README.md                 # This documentation
├── BUILD.md                  # Build instructions
├── windows/                  # Windows-specific build files
│   ├── EncoderUploader.spec  # PyInstaller configuration
│   ├── build_executable.bat  # Build script
│   ├── create_package.bat    # Distribution package creator
│   └── dist/                 # Built executable (after building)
│       └── EncoderUploader.exe
├── linux/                    # Linux build files (future)
├── macos/                    # macOS build files (future)
├── templates/
│   └── index.html            # Web interface template
├── static/
│   └── style.css            # Stylesheet
└── encoderData/
    ├── settings.json        # Application settings
    └── recordings/
        └── broadcast/       # Recording files location
```

## Configuration

The application creates an `encoderData` folder in the same directory as the executable containing:

- **settings.json**: Upload server URL configuration
- **recordings/broadcast/**: Location for MP4 recording files

## Upload Server Configuration

1. Click **Settings** in the application
2. Enter your upload server URL (e.g., `https://example.com/ajaxservices.php?rtmpkey=YOUR_KEY`)
3. Click **Save Settings**

## Overlapping Files Detection

The application automatically checks the upload server for overlapping files:

- **Green "No overlapping files"**: Safe to upload
- **Red timeline with bars**: Shows overlap periods visually
- **Red error message**: Server communication issues

## Dependencies

### Runtime (Built into Executable)
- Flask 2.3.3 - Web framework
- webview 4.4.1 - Native window integration
- requests 2.31.0 - HTTP client

### Build Tools
- PyInstaller 6.1.0 - Executable builder

## Technical Details

### Architecture
- **Flask Backend**: Handles file operations and server communication
- **Webview Frontend**: Provides native window with embedded browser
- **Threading**: Flask runs in background thread while webview manages UI

### Executable Packaging
- **Single File**: All dependencies bundled into one executable
- **No Installation**: Runs directly without Python installation
- **Windows Native**: Uses system browser engine for UI rendering

### Security
- **Local Only**: Flask server binds to 127.0.0.1 (localhost only)
- **Dynamic Port**: Automatically finds available port starting from 5000
- **Port Range**: Tries ports 5000-5009, displays selected port in console
- **File Validation**: Checks file existence and permissions
- **Safe Paths**: Uses secure filename handling

## Troubleshooting

### Build Issues

**"Python not found"**
- Install Python 3.7+ from python.org
- Ensure Python is in system PATH

**"PyInstaller failed"**
- Try: `pip install --upgrade pyinstaller`
- Check Windows Defender isn't blocking the build

**"Module not found"**
- Run: `pip install -r requirements.txt`
- Try: `pip install --upgrade pip`

### Runtime Issues

**"Application won't start"**
- Ensure `encoderData` folder exists in same directory as executable
- Check Windows Defender/antivirus isn't blocking the executable
- Try running as administrator
- Check console output for port assignment message

**"Port conflicts"**
- Application automatically finds available ports 5000-5009
- If all ports busy, try closing other applications using these ports
- Console will show: "Starting Flask server on port XXXX"

**"Upload fails"**
- Verify upload server URL in Settings
- Check internet connection
- Ensure server accepts the authentication key

**"Files not visible"**
- Check `encoderData/recordings/broadcast/` folder exists
- Ensure MP4 files are in the correct directory
- Verify file permissions

### Performance

**Large Files**
- Upload progress is shown with cancel option
- Large files may take time depending on connection speed
- Server timeout is set to 5 minutes

**Memory Usage**
- Application uses minimal memory (~50-100MB)
- Memory usage scales with number of files displayed

## Development

### Adding Features

1. Modify `main.py` for backend changes
2. Update `templates/index.html` for UI changes
3. Rebuild executable with `windows/build_executable.bat`

### Custom Icon

1. Create 256x256 pixel PNG/JPG image
2. Convert to ICO format
3. Save as `app_icon.ico`
4. Update `icon='app_icon.ico'` in `windows/EncoderUploader.spec`

## License

This project is part of the RPI Encoder suite. See main project for license details.
