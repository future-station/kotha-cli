@echo off
REM Kotha CLI Standalone Executable Builder
echo.
echo ============================================
echo   Kotha CLI Standalone Executable Builder
echo ============================================
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

echo Installing PyInstaller...
python -m pip install pyinstaller

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to install PyInstaller
    echo.
    pause
    exit /b 1
)

echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist kotha\__pycache__ rmdir /s /q kotha\__pycache__

echo.
echo Building standalone executable...
python -m PyInstaller kotha.spec

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to build executable
    echo.
    pause
    exit /b 1
)

echo.
echo Testing executable...
dist\kotha.exe --version

if %errorlevel% neq 0 (
    echo.
    echo Warning: Executable created but test failed
    echo.
) else (
    echo.
    echo ✅ Executable built and tested successfully!
    echo.
    echo 📍 Location: dist\kotha.exe
    echo.
    echo 📖 Next steps:
    echo 1. Copy dist\kotha.exe to your target machine
    echo 2. Add to PATH (optional): copy to C:\Windows\System32 or add folder to PATH
    echo 3. Set API key: kotha.exe --set-api="your-api-key"
    echo 4. Use anywhere: kotha.exe your-video.mp4
    echo.
)

pause
