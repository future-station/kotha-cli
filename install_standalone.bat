@echo off
REM Kotha CLI Standalone Installer
echo.
echo    ___  ___      _    _
echo   ^|_  ^|/ _ \    ^| ^|  ^| ^|
echo     ^| / /_\ \   ^| ^|__^| ^| __ _
echo     ^| ^|  _  ^|   ^|  __  ^|/ _` ^|
echo /\__/ / ^| ^| ^|   ^| ^|  ^| ^| (_^| ^|
echo \____/\_^| ^|_/   ^|_^|  ^|_^|\__,_^|
echo.
echo Kotha CLI Standalone Installer
echo ===============================
echo.

REM Check if kotha.exe exists
if not exist kotha.exe (
    echo Error: kotha.exe not found in current directory
    echo Please ensure kotha.exe is in the same folder as this installer
    echo.
    pause
    exit /b 1
)

echo Found kotha.exe - proceeding with installation...
echo.

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\kotha-cli
echo Creating installation directory: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
echo Copying kotha.exe to installation directory...
copy kotha.exe "%INSTALL_DIR%\" >nul

if %errorlevel% neq 0 (
    echo Error: Failed to copy kotha.exe
    echo.
    pause
    exit /b 1
)

REM Add to PATH for current user
echo Adding Kotha CLI to PATH...
set "NEW_PATH=%INSTALL_DIR%"

REM Check if already in PATH
echo %PATH% | findstr /I /C:"%NEW_PATH%" >nul
if %errorlevel% equ 0 (
    echo Kotha CLI is already in PATH
) else (
    REM Add to user PATH using PowerShell
    powershell -Command "$path = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($path -notlike '*%NEW_PATH%*') { [Environment]::SetEnvironmentVariable('PATH', $path + ';%NEW_PATH%', 'User') }"
    echo Added to PATH - you may need to restart your terminal
)

REM Test installation
echo.
echo Testing installation...
"%INSTALL_DIR%\kotha.exe" --version

if %errorlevel% neq 0 (
    echo Warning: Installation completed but test failed
    echo You can still use kotha by running: %INSTALL_DIR%\kotha.exe
    echo.
) else (
    echo.
    echo ✅ Installation completed successfully!
    echo.
)

echo 📖 Usage:
echo 1. Set your API key: kotha --set-api="your-gemini-api-key"
echo 2. Process videos: kotha your-video.mp4
echo 3. Get help: kotha --help
echo.
echo 📍 Installed to: %INSTALL_DIR%\kotha.exe
echo.
echo Note: You may need to restart your command prompt to use 'kotha' from anywhere
echo.
pause
