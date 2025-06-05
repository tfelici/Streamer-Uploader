# macOS Build Instructions

This directory contains build files for creating a standalone macOS executable of the Encoder Uploader application.

## Prerequisites

### System Requirements
- macOS 10.14 (Mojave) or higher
- Python 3.7 or higher
- Xcode Command Line Tools

### Installation

**1. Install Xcode Command Line Tools:**
```bash
xcode-select --install
```

**2. Install Python 3 (if not already installed):**
```bash
# Using Homebrew (recommended)
brew install python

# OR download from python.org
# Visit https://www.python.org/downloads/macos/
```

**3. Install required Python packages:**
```bash
pip3 install pyobjc-framework-Cocoa pyobjc-framework-WebKit
```

## Building the Executable

1. **Navigate to the macos directory:**
   ```bash
   cd macos/
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

- **Executable**: `macos/dist/EncoderUploader` (~15-20MB)
- **Data Directory**: `macos/dist/encoderData/` (application data folder)

## Distribution

### For End Users
1. Copy the entire `dist/` folder to the target macOS system
2. Run the application: `./EncoderUploader`
3. **First Run**: You may need to right-click and select "Open" to bypass Gatekeeper

### Package Contents
```
dist/
├── EncoderUploader          # Main executable
└── encoderData/             # Data directory
    └── recordings/
        └── broadcast/       # Recording files location
```

## Code Signing (Optional)

For distribution, you may want to code sign the executable:

```bash
# Self-signed (for testing)
codesign --force --deep --sign - dist/EncoderUploader

# With developer certificate (for distribution)
codesign --force --deep --sign "Developer ID Application: Your Name" dist/EncoderUploader
```

## Runtime Requirements

The built executable includes all Python dependencies and should run on macOS systems without additional installation. The target system needs:

- macOS 10.14 or higher
- Standard system frameworks (Cocoa, WebKit)

## Troubleshooting

### Build Issues

**"Command not found: python3"**
- Install Python 3 from python.org or using Homebrew: `brew install python`

**"xcode-select: error: command line tools are not installed"**
- Install Command Line Tools: `xcode-select --install`

**"No module named 'objc'"**
- Install PyObjC: `pip3 install pyobjc-framework-Cocoa pyobjc-framework-WebKit`

**"ImportError: No module named '_ctypes'"**
- Reinstall Python with proper configuration or use Homebrew version

### Runtime Issues

**"EncoderUploader cannot be opened because it is from an unidentified developer"**
- Right-click the executable and select "Open"
- Or go to System Preferences → Security & Privacy → Allow anyway

**"Permission denied"**
- Make executable: `chmod +x EncoderUploader`
- Check directory permissions for `encoderData/`

**"Port already in use"**
- Application will automatically try ports 5000-5009
- Close other applications using these ports if needed

### Gatekeeper Issues

**For unsigned executables:**
1. Right-click → Open (instead of double-clicking)
2. Click "Open" in the security dialog
3. Alternatively, disable Gatekeeper temporarily: `sudo spctl --master-disable`

**For distribution:**
- Consider code signing with a Developer ID certificate
- Or provide clear instructions for users to bypass Gatekeeper

## Technical Notes

### PyInstaller Configuration
- Uses `EncoderUploader_onefile.spec` for build configuration
- Includes Cocoa and WebKit frameworks for native macOS integration
- Bundles Flask templates and static files
- Console mode enabled for debugging

### Dependencies Included
- Flask web framework
- webview (Cocoa backend for macOS)
- requests and requests-toolbelt
- pymediainfo for video file analysis
- PyObjC frameworks (Cocoa, WebKit)
- All Python standard library modules

### File Size Optimization
- UPX compression enabled (reduces file size by ~30%)
- Excludes unnecessary modules and files
- Single-file executable for easy distribution

### Architecture Support
- Built for the architecture of the build machine (x86_64 or arm64)
- Universal binaries require additional configuration
- Most modern Macs support both architectures via Rosetta 2
