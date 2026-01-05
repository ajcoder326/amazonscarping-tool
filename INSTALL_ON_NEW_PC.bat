@echo off
REM ===============================================================
REM Amazon Scraping Tool - New PC Installation Script
REM Downloads and sets up the complete tool from GitHub
REM ===============================================================

setlocal enabledelayedexpansion
title Amazon Scraping Tool - New PC Installation

echo.
echo ============================================================
echo    AMAZON SCRAPING TOOL - NEW PC INSTALLATION
echo ============================================================
echo.
echo This script will:
echo    1. Check if Git is installed
echo    2. Download the tool from GitHub
echo    3. Run the complete setup process
echo    4. Create desktop shortcuts
echo    5. Test the installation
echo.
echo Repository: https://github.com/ajcoder326/amazonscarping-tool
echo.
echo ============================================================
echo.
pause

REM Get installation directory (default: C:\AmazonScrapingTool)
set DEFAULT_DIR=C:\AmazonScrapingTool
set /p INSTALL_DIR="Enter installation directory (default: %DEFAULT_DIR%): "
if "%INSTALL_DIR%"=="" set INSTALL_DIR=%DEFAULT_DIR%

echo.
echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM ============================================================
REM Step 1: Check Git Installation
REM ============================================================
echo ============================================================
echo [STEP 1/6] Checking Git installation...
echo ============================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo    GIT NOT FOUND - DOWNLOADING PORTABLE VERSION
    echo ============================================================
    echo.
    
    REM Create temp directory for Git download
    set TEMP_DIR=%TEMP%\git_portable
    if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
    
    echo [INFO] Downloading Git Portable...
    echo [INFO] This may take a few minutes...
    
    REM Download Git Portable using PowerShell
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/PortableGit-2.43.0-64-bit.7z.exe' -OutFile '%TEMP_DIR%\git-portable.exe'}"
    
    if not exist "%TEMP_DIR%\git-portable.exe" (
        echo [ERROR] Failed to download Git Portable!
        echo.
        echo Please install Git manually:
        echo 1. Go to: https://git-scm.com/download/win
        echo 2. Download and install Git for Windows
        echo 3. Run this script again
        echo.
        pause
        exit /b 1
    )
    
    echo [INFO] Extracting Git Portable...
    "%TEMP_DIR%\git-portable.exe" -o"%TEMP_DIR%\git" -y
    
    REM Add Git to PATH for this session
    set PATH=%TEMP_DIR%\git\bin;%PATH%
    
    echo [OK] Git Portable ready!
) else (
    echo [OK] Git is already installed!
)

echo.

REM ============================================================
REM Step 2: Create Installation Directory
REM ============================================================
echo ============================================================
echo [STEP 2/6] Creating installation directory...
echo ============================================================
echo.

if exist "%INSTALL_DIR%" (
    echo [WARNING] Directory already exists: %INSTALL_DIR%
    set /p OVERWRITE="Do you want to overwrite it? (y/n): "
    if /i not "!OVERWRITE!"=="y" (
        echo [INFO] Installation cancelled by user
        pause
        exit /b 0
    )
    echo [INFO] Removing existing directory...
    rmdir /s /q "%INSTALL_DIR%"
)

mkdir "%INSTALL_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to create directory: %INSTALL_DIR%
    echo [INFO] Try running as Administrator or choose a different location
    pause
    exit /b 1
)

echo [OK] Installation directory created!
echo.

REM ============================================================
REM Step 3: Clone Repository
REM ============================================================
echo ============================================================
echo [STEP 3/6] Downloading Amazon Scraping Tool...
echo ============================================================
echo.

echo [INFO] Cloning from GitHub...
echo [INFO] Repository: https://github.com/ajcoder326/amazonscarping-tool.git
echo.

git clone https://github.com/ajcoder326/amazonscarping-tool.git "%INSTALL_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to clone repository!
    echo.
    echo Possible solutions:
    echo 1. Check internet connection
    echo 2. Verify repository URL
    echo 3. Try again later
    echo.
    pause
    exit /b 1
)

echo [OK] Repository downloaded successfully!
echo.

REM ============================================================
REM Step 4: Run Setup Script
REM ============================================================
echo ============================================================
echo [STEP 4/6] Running setup script...
echo ============================================================
echo.

cd /d "%INSTALL_DIR%"

echo [INFO] Starting automated setup...
echo [INFO] This will install Python packages and browsers...
echo.

call SETUP.bat
if errorlevel 1 (
    echo [ERROR] Setup script failed!
    echo [INFO] Please check the error messages above
    pause
    exit /b 1
)

echo [OK] Setup completed successfully!
echo.

REM ============================================================
REM Step 5: Create Desktop Shortcuts
REM ============================================================
echo ============================================================
echo [STEP 5/6] Creating desktop shortcuts...
echo ============================================================
echo.

set DESKTOP=%USERPROFILE%\Desktop

REM Create shortcut for Audit Tool
echo [INFO] Creating audit tool shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Amazon Audit Tool.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\run_audit.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%SystemRoot%\System32\shell32.dll,21'; $Shortcut.Description = 'Amazon Product Audit Tool'; $Shortcut.Save()}"

REM Create shortcut for Traffic Generator
echo [INFO] Creating traffic generator shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Amazon Traffic Generator.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\run_traffic_gui.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%SystemRoot%\System32\shell32.dll,14'; $Shortcut.Description = 'Amazon Traffic Generator GUI'; $Shortcut.Save()}"

REM Create shortcut for Test Installation
echo [INFO] Creating test shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Test Amazon Tool.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\test_setup.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%SystemRoot%\System32\shell32.dll,23'; $Shortcut.Description = 'Test Amazon Scraping Tool Installation'; $Shortcut.Save()}"

echo [OK] Desktop shortcuts created!
echo.

REM ============================================================
REM Step 6: Final Test
REM ============================================================
echo ============================================================
echo [STEP 6/6] Testing installation...
echo ============================================================
echo.

echo [INFO] Running quick installation test...

REM Test Python and packages
call venv\Scripts\activate.bat
python -c "import playwright; import pandas; import asyncio; print('[OK] All Python packages working!')"
if errorlevel 1 (
    echo [ERROR] Python package test failed!
    pause
    exit /b 1
)

REM Test Playwright browser
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); browser.close(); p.stop(); print('[OK] Playwright browser working!')"
if errorlevel 1 (
    echo [ERROR] Playwright browser test failed!
    pause
    exit /b 1
)

echo [OK] All tests passed!
echo.

REM ============================================================
REM Installation Complete
REM ============================================================
echo ============================================================
echo    INSTALLATION COMPLETED SUCCESSFULLY! 🎉
echo ============================================================
echo.
echo Amazon Scraping Tool has been installed to:
echo %INSTALL_DIR%
echo.
echo DESKTOP SHORTCUTS CREATED:
echo ✅ Amazon Audit Tool - Extract product data
echo ✅ Amazon Traffic Generator - Simulate user behavior  
echo ✅ Test Amazon Tool - Verify installation
echo.
echo QUICK START:
echo.
echo 1. AUDIT PRODUCTS:
echo    - Double-click "Amazon Audit Tool" on desktop
echo    - Select your ASIN file (Excel/CSV)
echo    - Let it run and extract data
echo.
echo 2. GENERATE TRAFFIC:
echo    - Double-click "Amazon Traffic Generator" on desktop
echo    - Use the GUI to simulate user behavior
echo.
echo 3. TEST INSTALLATION:
echo    - Double-click "Test Amazon Tool" on desktop
echo    - Verify everything works correctly
echo.
echo NEXT STEPS:
echo 1. Prepare your ASIN file (Excel/CSV format)
echo 2. Export Amazon cookies (see COOKIES_GUIDE.md)
echo 3. Configure proxies (optional)
echo 4. Start your first audit or traffic simulation!
echo.
echo DOCUMENTATION LOCATION:
echo %INSTALL_DIR%\README.md
echo %INSTALL_DIR%\DEPLOYMENT_GUIDE.md
echo %INSTALL_DIR%\QUICK_START.txt
echo.
echo ============================================================
echo.
echo 🚀 Happy scraping!
echo.
echo Installation directory: %INSTALL_DIR%
echo GitHub repository: https://github.com/ajcoder326/amazonscarping-tool
echo.
pause

REM Clean up temporary Git if we downloaded it
if exist "%TEMP%\git_portable" (
    echo [INFO] Cleaning up temporary files...
    rmdir /s /q "%TEMP%\git_portable" 2>nul
)

echo.
echo Installation complete! You can now close this window.
echo.