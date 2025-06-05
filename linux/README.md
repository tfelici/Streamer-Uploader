# Linux Build Instructions

This directory contains build files for creating a standalone Linux executable of the Streamer Uploader application.

## Prerequisites

### System Requirements
- Linux distribution (Ubuntu 18.04+, CentOS 7+, or equivalent)
- Python 3.7 or higher
- pip3 package manager

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install python3 python3-pip python3-gobject gtk3-devel webkit2gtk3-devel
# OR for newer versions:
sudo dnf install python3 python3-pip python3-gobject gtk3-devel webkit2gtk3-devel
```

## Building the Executable

1. **Navigate to the linux directory:**
   ```bash
   cd linux/
   ```

2. **Make the build script executable:**
   ```bash
   chmod +x build_standalone.sh
   ```

3. **Run the build script:**
   ```bash
   ./build_standalone.sh
   ```

## Build Output

After a successful build, you'll find:

- **Executable**: `linux/dist/StreamerUploader` (~15-20MB)
- **Data Directory**: `linux/dist/streamerData/` (application data folder)

## Distribution

### For End Users
1. Copy the entire `dist/` folder to the target Linux system
2. Make sure the executable has run permissions: `chmod +x StreamerUploader`
3. Run the application: `./StreamerUploader`

### Package Contents
```
dist/
├── StreamerUploader          # Main executable
└── streamerData/             # Data directory
    └── recordings/
        └── broadcast/       # Recording files location
```

## Runtime Requirements

The built executable includes all Python dependencies and should run on most Linux systems without additional installation. However, the target system needs:

- GTK 3.0 libraries (usually pre-installed)
- WebKit2GTK libraries (for the web interface)
- Standard C libraries

## Troubleshooting

### Build Issues

**"Command not found: python3"**
- Install Python 3: `sudo apt-get install python3` (Ubuntu) or `sudo yum install python3` (CentOS)

**"No module named 'gi'"**
- Install GObject Introspection: `sudo apt-get install python3-gi`

**"WebKit2 not found"**
- Install WebKit: `sudo apt-get install gir1.2-webkit2-4.0`

### Runtime Issues

**"Failed to load webview"**
- Ensure GTK and WebKit libraries are installed on target system
- Try installing: `sudo apt-get install libgtk-3-0 libwebkit2gtk-4.0-37`

**"Permission denied"**
- Make executable: `chmod +x StreamerUploader`
- Check directory permissions for `streamerData/`

**"Port already in use"**
- Application will automatically try ports 5000-5009
- Close other applications using these ports if needed

## Technical Notes

### PyInstaller Configuration
- Uses `StreamerUploader_onefile.spec` for build configuration
- Includes all webview backends (GTK, Qt, CEF) for maximum compatibility
- Bundles Flask templates and static files
- Console mode enabled for debugging

### Dependencies Included
- Flask web framework
- webview (PyGObject backend for Linux)
- requests and requests-toolbelt
- pymediainfo for video file analysis
- All Python standard library modules

### File Size Optimization
- UPX compression enabled (reduces file size by ~30%)
- Excludes unnecessary modules and files
- Single-file executable for easy distribution
