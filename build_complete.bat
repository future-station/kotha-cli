@echo off
REM Complete Kotha CLI Distribution Builder
echo.
echo ================================================
echo   Kotha CLI Complete Distribution Builder
echo ================================================
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

echo Step 1: Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Step 2: Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist kotha-cli-standalone rmdir /s /q kotha-cli-standalone
if exist __pycache__ rmdir /s /q __pycache__
if exist kotha\__pycache__ rmdir /s /q kotha\__pycache__

echo.
echo Step 3: Building standalone executable...
python -m PyInstaller kotha.spec

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo Step 4: Testing executable...
dist\kotha.exe --version

if %errorlevel% neq 0 (
    echo.
    echo Warning: Executable created but test failed
)

echo.
echo Step 5: Creating distribution package...
mkdir kotha-cli-standalone
copy dist\kotha.exe kotha-cli-standalone\
copy install_standalone.bat kotha-cli-standalone\
copy README_STANDALONE.md kotha-cli-standalone\

echo.
echo Step 6: Creating distribution archive...
powershell Compress-Archive -Path "kotha-cli-standalone\*" -DestinationPath "kotha-cli-standalone-v1.0.0.zip" -Force

echo.
echo ✅ Build completed successfully!
echo.
echo 📦 Distribution files:
echo   - kotha-cli-standalone\ (folder)
echo   - kotha-cli-standalone-v1.0.0.zip (archive)
echo.
echo 📖 To distribute:
echo   1. Share the ZIP file or the standalone folder
echo   2. Recipients run install_standalone.bat
echo   3. No Python installation required!
echo.
echo 📏 Executable size:
for %%A in (dist\kotha.exe) do echo   %%~zA bytes (%%~zA
echo.
pause
