@echo off
echo Building Encoder Uploader Standalone Executable...
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
python -m PyInstaller EncoderUploader_onefile.spec
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

REM Create directory structure for standalone version
echo Setting up distribution structure...
if not exist "dist\EncoderUploader_Standalone" mkdir "dist\EncoderUploader_Standalone"
if not exist "dist\EncoderUploader_Standalone\encoderData" mkdir "dist\EncoderUploader_Standalone\encoderData"
if not exist "dist\EncoderUploader_Standalone\encoderData\recordings" mkdir "dist\EncoderUploader_Standalone\encoderData\recordings"
if not exist "dist\EncoderUploader_Standalone\encoderData\recordings\broadcast" mkdir "dist\EncoderUploader_Standalone\encoderData\recordings\broadcast"

REM Move the standalone executable
move "dist\EncoderUploader_Standalone.exe" "dist\EncoderUploader_Standalone\EncoderUploader_Standalone.exe"

REM Copy existing settings if they exist
if exist "encoderData\settings.json" copy "encoderData\settings.json" "dist\EncoderUploader_Standalone\encoderData\settings.json"

REM Copy existing recordings if they exist
if exist "encoderData\recordings\broadcast\*.mp4" copy "encoderData\recordings\broadcast\*.mp4" "dist\EncoderUploader_Standalone\encoderData\recordings\broadcast\"

echo.
echo ====================================================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ====================================================================
echo.
echo Standalone executable created:
echo Location: dist\EncoderUploader_Standalone\EncoderUploader_Standalone.exe
echo.
echo Distribution: Copy the entire 'EncoderUploader_Standalone' folder
echo.
echo Features included:
echo - Self-contained single executable (no Python required)
echo - Integrated web browser viewer
echo - Recording upload functionality  
echo - Settings management
echo - Overlapping files detection
echo - All dependencies bundled
echo.
echo The 'encoderData' folder structure is already set up.
echo.
pause
