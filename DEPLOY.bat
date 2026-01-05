@echo off
REM ===============================================================
REM Amazon Audit Tool - Complete One-Click Deployment
REM Run this ONCE on a fresh Windows server
REM ===============================================================

setlocal enabledelayedexpansion
title Amazon Audit Tool - Deployment

echo.
echo ============================================================
echo    AMAZON AUDIT TOOL - ONE-CLICK DEPLOYMENT
echo ============================================================
echo.
echo This script will:
echo    1. Check Python installation
echo    2. Create virtual environment
echo    3. Install all required packages
echo    4. Install Playwright browser
echo    5. Download and configure ngrok
echo    6. Create startup scripts
echo.
echo ============================================================
echo.
pause

REM Get the directory where this bat file is located
set APP_DIR=%~dp0
cd /d "%APP_DIR%"
set APP_DIR=%CD%

echo.
echo [INFO] Application directory: %APP_DIR%
echo.

REM ============================================================
REM Step 1: Check Python
REM ============================================================
echo ============================================================
echo [STEP 1/6] Checking Python installation...
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo    ERROR: PYTHON NOT FOUND!
    echo ============================================================
    echo.
    echo Please install Python 3.10 or higher:
    echo    1. Go to: https://python.org/downloads
    echo    2. Download Python 3.10+
    echo    3. Run installer
    echo    4. IMPORTANT: Check "Add Python to PATH"
    echo    5. Click "Install Now"
    echo    6. Run this script again
    echo.
    echo ============================================================
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo    [OK] Python %PYTHON_VER% found!
echo.

REM ============================================================
REM Step 2: Create Virtual Environment
REM ============================================================
echo ============================================================
echo [STEP 2/6] Creating Python virtual environment...
echo ============================================================
echo.

if exist "%APP_DIR%\venv" (
    echo    [INFO] Virtual environment already exists
    echo    [INFO] Removing old environment...
    rmdir /s /q "%APP_DIR%\venv"
)

echo    [INFO] Creating new virtual environment...
python -m venv "%APP_DIR%\venv"

if errorlevel 1 (
    echo    [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

echo    [OK] Virtual environment created!
echo.

REM Activate virtual environment
call "%APP_DIR%\venv\Scripts\activate.bat"

REM ============================================================
REM Step 3: Install Python Packages
REM ============================================================
echo ============================================================
echo [STEP 3/6] Installing Python packages...
echo ============================================================
echo.
echo    This may take 2-5 minutes...
echo.

python -m pip install --upgrade pip --quiet

echo    Installing Flask...
pip install flask --quiet
echo    Installing Pandas...
pip install pandas --quiet
echo    Installing Openpyxl...
pip install openpyxl --quiet
echo    Installing Playwright...
pip install playwright --quiet
echo    Installing Waitress...
pip install waitress --quiet
echo    Installing Aiofiles...
pip install aiofiles --quiet
echo    Installing Pyexcel...
pip install pyexcel pyexcel-ods --quiet

echo.
echo    [OK] All packages installed!
echo.

REM ============================================================
REM Step 4: Install Playwright Browser
REM ============================================================
echo ============================================================
echo [STEP 4/6] Installing Playwright Chromium browser...
echo ============================================================
echo.
echo    This may take 2-5 minutes (downloads ~150MB)...
echo.

playwright install chromium

if errorlevel 1 (
    echo    [WARNING] Playwright browser installation had issues
    echo    [INFO] Trying alternative method...
    python -m playwright install chromium
)

echo.
echo    [OK] Playwright browser installed!
echo.

REM ============================================================
REM Step 5: Download and Configure ngrok
REM ============================================================
echo ============================================================
echo [STEP 5/6] Setting up ngrok...
echo ============================================================
echo.

if not exist "%APP_DIR%\tools" mkdir "%APP_DIR%\tools"

if not exist "%APP_DIR%\tools\ngrok.exe" (
    echo    [INFO] Downloading ngrok...
    echo.
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile '%APP_DIR%\tools\ngrok.zip'}"
    
    if exist "%APP_DIR%\tools\ngrok.zip" (
        echo    [INFO] Extracting ngrok...
        powershell -Command "Expand-Archive -Path '%APP_DIR%\tools\ngrok.zip' -DestinationPath '%APP_DIR%\tools' -Force"
        del "%APP_DIR%\tools\ngrok.zip" 2>nul
        echo    [OK] ngrok downloaded!
    ) else (
        echo    [ERROR] Failed to download ngrok!
        echo    [INFO] Please download manually from: https://ngrok.com/download
        pause
    )
) else (
    echo    [OK] ngrok already installed!
)

echo.
echo ============================================================
echo    NGROK AUTHENTICATION REQUIRED
echo ============================================================
echo.
echo To get your ngrok auth token:
echo    1. Go to: https://dashboard.ngrok.com/get-started/your-authtoken
echo    2. Sign up or log in
echo    3. Copy your auth token
echo.
set /p NGROK_TOKEN="Paste your ngrok auth token here: "

if "%NGROK_TOKEN%"=="" (
    echo    [WARNING] No token entered. You can configure later.
) else (
    echo.
    echo    [INFO] Configuring ngrok...
    "%APP_DIR%\tools\ngrok.exe" config add-authtoken %NGROK_TOKEN%
    echo    [OK] ngrok configured!
)

echo.
echo ============================================================
echo    NGROK DOMAIN (Optional)
echo ============================================================
echo.
echo If you have a static ngrok domain, enter it now.
echo Example: your-name.ngrok-free.dev
echo Press Enter to skip (will use random URL)
echo.
set /p NGROK_DOMAIN="Enter your ngrok domain (or press Enter to skip): "

echo.

REM ============================================================
REM Step 6: Create Startup Scripts
REM ============================================================
echo ============================================================
echo [STEP 6/6] Creating startup scripts...
echo ============================================================
echo.

REM Create START.bat (the main startup script)
(
echo @echo off
echo title Amazon Audit Tool
echo.
echo echo ============================================================
echo echo    AMAZON AUDIT TOOL - Starting...
echo echo ============================================================
echo echo.
echo.
echo cd /d "%APP_DIR%"
echo.
echo echo [1/2] Starting server...
echo start "Audit Tool Server" cmd /k "cd /d "%APP_DIR%" && call venv\Scripts\activate.bat && set PYTHONPATH=%APP_DIR% && python -m waitress --host=0.0.0.0 --port=5000 --threads=8 web_app.app:app"
echo.
echo echo [INFO] Waiting for server to start...
echo timeout /t 5 /nobreak ^>nul
echo.
echo echo [2/2] Starting ngrok tunnel...
) > "%APP_DIR%\START.bat"

if "%NGROK_DOMAIN%"=="" (
    echo start "ngrok Tunnel" cmd /k ""%APP_DIR%\tools\ngrok.exe" http 5000" >> "%APP_DIR%\START.bat"
) else (
    echo start "ngrok Tunnel" cmd /k ""%APP_DIR%\tools\ngrok.exe" http 5000 --domain=%NGROK_DOMAIN%" >> "%APP_DIR%\START.bat"
)

(
echo.
echo echo.
echo echo ============================================================
echo echo    READY!
echo echo ============================================================
echo echo.
if "%NGROK_DOMAIN%"=="" (
echo echo Your tool is running! Check the ngrok window for your URL.
) else (
echo echo Your tool is accessible at:
echo echo    https://%NGROK_DOMAIN%
)
echo echo.
echo echo Share this link with your users!
echo echo.
echo echo To stop: Close the server and ngrok windows
echo echo ============================================================
echo echo.
echo pause
) >> "%APP_DIR%\START.bat"

REM Create STOP.bat
(
echo @echo off
echo title Amazon Audit Tool - Stopping
echo echo.
echo echo Stopping Amazon Audit Tool...
echo echo.
echo taskkill /f /im python.exe 2^>nul
echo taskkill /f /im ngrok.exe 2^>nul
echo echo.
echo echo [OK] All processes stopped!
echo echo.
echo timeout /t 3
) > "%APP_DIR%\STOP.bat"

echo    [OK] START.bat created!
echo    [OK] STOP.bat created!
echo.

REM ============================================================
REM Complete!
REM ============================================================
echo.
echo ============================================================
echo    DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo    Files created:
echo       START.bat - Double-click to start the tool
echo       STOP.bat  - Double-click to stop the tool
echo.
echo ============================================================
echo    HOW TO USE:
echo ============================================================
echo.
echo    1. Double-click START.bat
echo    2. Two windows will open (server + ngrok)
if "%NGROK_DOMAIN%"=="" (
echo    3. Check ngrok window for your public URL
) else (
echo    3. Access at: https://%NGROK_DOMAIN%
)
echo    4. Share the URL with your users!
echo.
echo ============================================================
echo.
set /p START_NOW="Do you want to start the tool now? (Y/N): "
if /i "%START_NOW%"=="Y" (
    echo.
    echo Starting...
    start "" "%APP_DIR%\START.bat"
)
echo.
echo Deployment finished! Press any key to close...
pause >nul
