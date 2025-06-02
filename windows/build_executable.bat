@echo off
echo Building Encoder Uploader standalone executable...
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

REM Build the executable
echo Building executable with PyInstaller...
python -m PyInstaller EncoderUploader.spec
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

REM Copy necessary data files to dist folder
echo Copying data files...
if not exist "dist\encoderData" mkdir "dist\encoderData"
if not exist "dist\encoderData\recordings" mkdir "dist\encoderData\recordings"
if not exist "dist\encoderData\recordings\broadcast" mkdir "dist\encoderData\recordings\broadcast"

REM Copy existing settings if they exist
if exist "encoderData\settings.json" copy "encoderData\settings.json" "dist\encoderData\settings.json"

REM Copy existing recordings if they exist
if exist "encoderData\recordings\broadcast\*.mp4" copy "encoderData\recordings\broadcast\*.mp4" "dist\encoderData\recordings\broadcast\"

echo.
echo Build completed successfully!
echo Executable location: dist\EncoderUploader.exe
echo.
echo The executable includes:
echo - Integrated web browser viewer
echo - All Flask templates and static files
echo - Recording upload functionality
echo - Settings management
echo - Overlapping files detection
echo.
echo To distribute, copy the entire 'dist' folder to target machines.
echo The 'encoderData' folder will be created automatically if it doesn't exist.
echo.
pause
