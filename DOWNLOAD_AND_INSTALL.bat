@echo off
REM ===============================================================
REM Amazon Scraping Tool - Download and Install Script
REM This script downloads the installer and runs it
REM ===============================================================

title Amazon Scraping Tool - Download and Install

echo.
echo ============================================================
echo    AMAZON SCRAPING TOOL - DOWNLOAD AND INSTALL
echo ============================================================
echo.
echo This script will:
echo    1. Download the installation script from GitHub
echo    2. Run the complete installation process
echo.
echo Repository: https://github.com/ajcoder326/amazonscarping-tool
echo.
echo ============================================================
echo.
pause

REM Create temp directory
set TEMP_DIR=%TEMP%\amazon_scraping_tool_installer
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo [INFO] Downloading installation script...
echo.

REM Download the installation script using PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ajcoder326/amazonscarping-tool/master/INSTALL_ON_NEW_PC.bat' -OutFile '%TEMP_DIR%\INSTALL_ON_NEW_PC.bat' } catch { Write-Host 'Download failed. Please check internet connection.'; exit 1 }}"

if not exist "%TEMP_DIR%\INSTALL_ON_NEW_PC.bat" (
    echo [ERROR] Failed to download installation script!
    echo.
    echo Please check:
    echo 1. Internet connection
    echo 2. Firewall settings
    echo 3. Repository availability
    echo.
    echo Manual download:
    echo 1. Go to: https://github.com/ajcoder326/amazonscarping-tool
    echo 2. Download INSTALL_ON_NEW_PC.bat
    echo 3. Run it manually
    echo.
    pause
    exit /b 1
)

echo [OK] Installation script downloaded!
echo.
echo [INFO] Starting installation process...
echo.

REM Run the installation script
call "%TEMP_DIR%\INSTALL_ON_NEW_PC.bat"

REM Clean up
echo.
echo [INFO] Cleaning up temporary files...
rmdir /s /q "%TEMP_DIR%" 2>nul

echo.
echo [OK] Installation process completed!
pause