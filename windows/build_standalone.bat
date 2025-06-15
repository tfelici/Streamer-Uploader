@echo off
echo Building Streamer Uploader Standalone Executable...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install -r ../requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install required packages
    pause
    exit /b 1
)

REM Ensure PyInstaller is properly installed
echo Ensuring PyInstaller is available...
pip install --upgrade pyinstaller>=6.0.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to install/upgrade PyInstaller
    pause
    exit /b 1
)

REM Clean previous build
echo Cleaning previous build...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo ====================================================================
echo Building standalone executable (single .exe, no dependencies)
echo ====================================================================
echo.

REM Build the standalone executable
echo Building standalone executable with PyInstaller...
echo Command: python -m PyInstaller StreamerUploader_onefile.spec
python -m PyInstaller StreamerUploader_onefile.spec
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed
    echo.
    echo Common issues:
    echo - Missing dependencies in requirements.txt
    echo - Import errors in main.py or utils.py
    echo - Missing template or static files
    echo.
    echo Please check the output above for specific error messages
    pause
    exit /b 1
)

REM Create directory structure for distribution
echo Setting up distribution structure...
if not exist "dist" mkdir "dist"

REM Check if the standalone executable was created successfully
if not exist "dist\StreamerUploader_Standalone.exe" (
    echo ERROR: Standalone executable was not created successfully
    echo Please check the PyInstaller output above for errors
    pause
    exit /b 1
)

REM Move the standalone executable to dist folder
move "dist\StreamerUploader_Standalone.exe" "dist\StreamerUploader.exe"

echo.
echo ====================================================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ====================================================================
echo.
echo Standalone executable created:
echo Location: windows\dist\StreamerUploader.exe
echo Release Package: windows\StreamerUploader_Windows.zip (ready for distribution)
echo.
echo Features included:
echo - Self-contained single executable (no Python required)
echo - Integrated web browser viewer
echo - Recording upload functionality with progress tracking
echo - Settings management
echo - Overlapping files detection
echo - Safe file removal for USB drives
echo - Video duration detection with pymediainfo
echo - All dependencies bundled (Flask, requests, pywebview, etc.)
echo.
echo The 'streamerData' folder structure is already set up.
echo Settings and recordings will be preserved if they exist.
echo.
echo To test the build:
echo 1. Navigate to the 'dist' folder
echo 2. Run 'StreamerUploader.exe'
echo 3. Configure upload URL in settings
echo 4. Test upload functionality
echo.
pause
