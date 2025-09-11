@echo off
echo Building Streamer Uploader Executable...
echo.

REM Navigate to the correct directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Install/upgrade required packages
echo Installing required packages...
pip install -r ../requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install required packages
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous build...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo ====================================================================
echo Building StreamerUploader.exe (no console, with splash screen)
echo ====================================================================
echo.

REM Build using the spec file you created
echo Building executable with PyInstaller...
python -m PyInstaller StreamerUploader.spec --noconfirm --clean
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed
    echo Please check the output above for error messages
    pause
    exit /b 1
)

REM Check if the executable was created successfully
if not exist "dist\StreamerUploader.exe" (
    echo ERROR: StreamerUploader.exe was not created successfully
    echo Please check the PyInstaller output above for errors
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ====================================================================
echo.
echo Executable created: windows\dist\StreamerUploader.exe
echo Size: 
dir dist\StreamerUploader.exe | findstr StreamerUploader.exe
echo.
echo Features included:
echo - Self-contained executable (no Python required)
echo - No console window (GUI only)
echo - Integrated web browser viewer
echo - Recording upload functionality with progress tracking
echo - Splash screen on startup
echo - All dependencies bundled
echo.
echo You can now run StreamerUploader.exe without Python installed.
echo.
pause