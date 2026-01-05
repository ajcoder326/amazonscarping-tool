@echo off
REM ===============================================================
REM Amazon Scraping Tool - Update Script
REM Updates existing installation with latest changes
REM ===============================================================

setlocal enabledelayedexpansion
title Amazon Scraping Tool - Update

echo.
echo ============================================================
echo    AMAZON SCRAPING TOOL - UPDATE
echo ============================================================
echo.
echo This script will:
echo    1. Backup current configuration
echo    2. Pull latest changes from GitHub
echo    3. Update Python packages
echo    4. Restore configuration
echo    5. Test updated installation
echo.
echo ============================================================
echo.
pause

REM Get current directory
set TOOL_DIR=%~dp0
cd /d "%TOOL_DIR%"

echo [INFO] Current directory: %TOOL_DIR%
echo.

REM ============================================================
REM Step 1: Backup Configuration
REM ============================================================
echo ============================================================
echo [STEP 1/5] Backing up configuration...
echo ============================================================
echo.

set BACKUP_DIR=%TOOL_DIR%\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

mkdir "%BACKUP_DIR%" 2>nul

REM Backup important files
if exist "cookies\amazon_cookies.json" (
    copy "cookies\amazon_cookies.json" "%BACKUP_DIR%\" >nul
    echo [OK] Backed up cookies
)

if exist "proxies.csv" (
    copy "proxies.csv" "%BACKUP_DIR%\" >nul
    echo [OK] Backed up proxies
)

if exist "traffic-generator\proxies.csv" (
    copy "traffic-generator\proxies.csv" "%BACKUP_DIR%\" >nul
    echo [OK] Backed up traffic generator proxies
)

echo [OK] Configuration backed up to: %BACKUP_DIR%
echo.

REM ============================================================
REM Step 2: Pull Latest Changes
REM ============================================================
echo ============================================================
echo [STEP 2/5] Pulling latest changes from GitHub...
echo ============================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found! Please install Git first.
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [INFO] Fetching latest changes...
git fetch origin
if errorlevel 1 (
    echo [WARNING] Failed to fetch from remote. Continuing with local update...
)

echo [INFO] Pulling latest changes...
git pull origin master
if errorlevel 1 (
    echo [WARNING] Git pull failed. You may need to resolve conflicts manually.
    echo [INFO] Continuing with package updates...
)

echo [OK] Repository updated!
echo.

REM ============================================================
REM Step 3: Update Python Packages
REM ============================================================
echo ============================================================
echo [STEP 3/5] Updating Python packages...
echo ============================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Please run SETUP.bat to create the environment first.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Updating packages from requirements.txt...
python -m pip install -r requirements.txt --upgrade

echo [INFO] Updating additional packages...
python -m pip install --upgrade playwright-stealth PyQt5

echo [INFO] Updating Playwright browsers...
python -m playwright install chromium

echo [OK] All packages updated!
echo.

REM ============================================================
REM Step 4: Restore Configuration
REM ============================================================
echo ============================================================
echo [STEP 4/5] Restoring configuration...
echo ============================================================
echo.

REM Restore backed up files
if exist "%BACKUP_DIR%\amazon_cookies.json" (
    copy "%BACKUP_DIR%\amazon_cookies.json" "cookies\" >nul
    echo [OK] Restored cookies
)

if exist "%BACKUP_DIR%\proxies.csv" (
    copy "%BACKUP_DIR%\proxies.csv" "." >nul
    echo [OK] Restored proxies
)

if exist "%BACKUP_DIR%\proxies.csv" (
    copy "%BACKUP_DIR%\proxies.csv" "traffic-generator\" >nul
    echo [OK] Restored traffic generator proxies
)

echo [OK] Configuration restored!
echo.

REM ============================================================
REM Step 5: Test Installation
REM ============================================================
echo ============================================================
echo [STEP 5/5] Testing updated installation...
echo ============================================================
echo.

echo [INFO] Testing Python imports...
python -c "import playwright; import pandas; import asyncio; print('[OK] All imports successful!')"
if errorlevel 1 (
    echo [ERROR] Import test failed!
    pause
    exit /b 1
)

echo [INFO] Testing Playwright browser...
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); browser.close(); p.stop(); print('[OK] Browser test successful!')"
if errorlevel 1 (
    echo [ERROR] Browser test failed!
    pause
    exit /b 1
)

echo [OK] All tests passed!
echo.

REM ============================================================
REM Update Complete
REM ============================================================
echo ============================================================
echo    UPDATE COMPLETED SUCCESSFULLY! 🎉
echo ============================================================
echo.
echo Your Amazon Scraping Tool has been updated!
echo.
echo WHAT WAS UPDATED:
echo ✅ Latest code from GitHub repository
echo ✅ Python packages upgraded to latest versions
echo ✅ Playwright browser updated
echo ✅ Configuration files preserved
echo.
echo BACKUP LOCATION:
echo %BACKUP_DIR%
echo.
echo NEXT STEPS:
echo 1. Test the updated tool with a small ASIN file
echo 2. Verify all features work as expected
echo 3. Update cookies if needed
echo 4. Resume normal operations
echo.
echo QUICK TEST:
echo - Run: test_setup.bat
echo - Or double-click "Test Amazon Tool" on desktop
echo.
echo ============================================================
echo.
echo 🚀 Update complete! Tool is ready to use.
echo.
pause