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

REM Create directory structure for distribution
echo Setting up distribution structure...
if not exist "dist" mkdir "dist"
if not exist "dist\encoderData" mkdir "dist\encoderData"
if not exist "dist\encoderData\recordings" mkdir "dist\encoderData\recordings"
if not exist "dist\encoderData\recordings\broadcast" mkdir "dist\encoderData\recordings\broadcast"

REM Move the standalone executable to dist folder
move "dist\EncoderUploader_Standalone.exe" "dist\EncoderUploader.exe"

REM Copy existing settings if they exist
if exist "encoderData\settings.json" copy "encoderData\settings.json" "dist\encoderData\settings.json"

REM Copy existing recordings if they exist
if exist "encoderData\recordings\broadcast\*.mp4" copy "encoderData\recordings\broadcast\*.mp4" "dist\encoderData\recordings\broadcast\"

REM Create a release package (ZIP file for easy distribution)
echo Creating release package...
powershell -Command "Compress-Archive -Path 'dist' -DestinationPath 'EncoderUploader_Windows.zip' -Force"

echo.
echo ====================================================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ====================================================================
echo.
echo Standalone executable created:
echo Location: windows\dist\EncoderUploader.exe
echo Release Package: windows\EncoderUploader_Windows.zip (ready for distribution)
echo.
echo Distribution Options:
echo 1. Copy the entire 'dist' folder
echo 2. Share the 'EncoderUploader_Windows.zip' file
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
