@echo off
REM Kotha CLI Windows Installer
echo.
echo    ___  ___      _    _
echo   ^|_  ^|/ _ \    ^| ^|  ^| ^|
echo     ^| / /_\ \   ^| ^|__^| ^| __ _
echo     ^| ^|  _  ^|   ^|  __  ^|/ _` ^|
echo /\__/ / ^| ^| ^|   ^| ^|  ^| ^| (_^| ^|
echo \____/\_^| ^|_/   ^|_^|  ^|_^|\__,_^|
echo.
echo Kotha CLI - Video to Text Transcription Tool
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo Installing Kotha CLI...
python -m pip install --upgrade pip
python -m pip install kotha-cli

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to install Kotha CLI
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo Testing installation...
kotha --version

if %errorlevel% neq 0 (
    echo.
    echo Warning: Installation completed but 'kotha' command not found in PATH.
    echo You may need to restart your terminal or add Python Scripts to PATH.
    echo.
) else (
    echo.
    echo ✅ Installation completed successfully!
    echo.
)

echo 📖 Next steps:
echo 1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
echo 2. Set your API key: kotha --set-api="your-api-key-here"
echo 3. Start using: kotha your-video.mp4
echo.
echo 💡 For help: kotha --help
echo.
pause
