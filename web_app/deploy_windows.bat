@echo off
REM ===============================================================
REM Amazon Audit Tool - Windows 10 Server One-Click Deployment
REM Domain: horal-agnes-acetated.ngrok-free.dev
REM ===============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo    AMAZON AUDIT TOOL - Windows 10 Server Deployment
echo ============================================================
echo.

REM Get script and app directories
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%.."
set APP_DIR=%CD%

set NGROK_DOMAIN=horal-agnes-acetated.ngrok-free.dev
set NGROK_AUTHTOKEN=2xTQsa09A1r16K6rfkQpT87RAw3_5EERz7pZ1qkj9hmXNK2ow

echo    Application Path: %APP_DIR%
echo.

REM ============================================================
REM Step 1: Check Python
REM ============================================================
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo    ERROR: Python is not installed!
    echo    Please install Python 3.10+ from: https://python.org
    echo    IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo        Python %PYTHON_VER% found

REM ============================================================
REM Step 2: Create Virtual Environment
REM ============================================================
echo.
echo [2/7] Setting up virtual environment...
if not exist "%APP_DIR%\server_venv" (
    python -m venv "%APP_DIR%\server_venv"
    echo        Created new virtual environment
) else (
    echo        Virtual environment exists
)
call "%APP_DIR%\server_venv\Scripts\activate.bat"
echo        Activated

REM ============================================================
REM Step 3: Install Python Packages
REM ============================================================
echo.
echo [3/7] Installing Python packages (this may take a few minutes)...
pip install --upgrade pip --quiet 2>nul
pip install flask playwright openpyxl pandas waitress --quiet 2>nul
echo        Packages installed

REM ============================================================
REM Step 4: Install Playwright Browsers
REM ============================================================
echo.
echo [4/7] Installing Playwright Chromium browser...
playwright install chromium 2>nul
echo        Browser installed

REM ============================================================
REM Step 5: Download ngrok
REM ============================================================
echo.
echo [5/7] Setting up ngrok...
if not exist "%APP_DIR%\tools" mkdir "%APP_DIR%\tools"

if not exist "%APP_DIR%\tools\ngrok.exe" (
    echo        Downloading ngrok...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile '%APP_DIR%\tools\ngrok.zip'}" 2>nul
    powershell -Command "Expand-Archive -Path '%APP_DIR%\tools\ngrok.zip' -DestinationPath '%APP_DIR%\tools' -Force" 2>nul
    del "%APP_DIR%\tools\ngrok.zip" 2>nul
    echo        Downloaded
) else (
    echo        Already installed
)

REM ============================================================
REM Step 6: Configure ngrok
REM ============================================================
echo.
echo [6/7] Configuring ngrok with your auth token...
"%APP_DIR%\tools\ngrok.exe" config add-authtoken %NGROK_AUTHTOKEN% 2>nul
echo        Configured

REM ============================================================
REM Step 7: Create Startup Scripts
REM ============================================================
echo.
echo [7/7] Creating startup scripts...

REM Server startup script
> "%APP_DIR%\START_SERVER.bat" (
    echo @echo off
    echo title Amazon Audit Tool - Server
    echo cd /d "%APP_DIR%"
    echo set PYTHONPATH=%APP_DIR%
    echo call "%APP_DIR%\server_venv\Scripts\activate.bat"
    echo echo.
    echo echo ============================================================
    echo echo    Amazon Audit Tool - Server Running
    echo echo ============================================================
    echo echo.
    echo echo Server starting on port 5000...
    echo echo.
    echo python -m waitress --host=0.0.0.0 --port=5000 --threads=8 web_app.app:app
)

REM ngrok startup script
> "%APP_DIR%\START_NGROK.bat" (
    echo @echo off
    echo title Amazon Audit Tool - ngrok Tunnel
    echo echo.
    echo echo ============================================================
    echo echo    ngrok Tunnel - Connecting...
    echo echo ============================================================
    echo echo.
    echo echo Domain: https://%NGROK_DOMAIN%
    echo echo.
    echo "%APP_DIR%\tools\ngrok.exe" http 5000 --domain=%NGROK_DOMAIN%
)

REM Combined startup script
> "%APP_DIR%\START_ALL.bat" (
    echo @echo off
    echo title Amazon Audit Tool
    echo echo.
    echo echo ============================================================
    echo echo    Starting Amazon Audit Tool...
    echo echo ============================================================
    echo echo.
    echo echo Step 1: Starting server...
    echo start "Audit Server" "%APP_DIR%\START_SERVER.bat"
    echo timeout /t 5 /nobreak ^>nul
    echo echo Step 2: Starting ngrok tunnel...
    echo start "ngrok Tunnel" "%APP_DIR%\START_NGROK.bat"
    echo echo.
    echo echo ============================================================
    echo echo    READY! Tool is accessible at:
    echo echo.
    echo echo    https://%NGROK_DOMAIN%
    echo echo.
    echo echo    Share this link with your users!
    echo echo ============================================================
    echo echo.
    echo echo Press any key to close this window...
    echo pause ^>nul
)

REM Stop script
> "%APP_DIR%\STOP_ALL.bat" (
    echo @echo off
    echo echo Stopping Amazon Audit Tool...
    echo taskkill /f /im python.exe 2^>nul
    echo taskkill /f /im ngrok.exe 2^>nul
    echo echo.
    echo echo Stopped!
    echo timeout /t 2 /nobreak ^>nul
)

echo        Scripts created

REM ============================================================
REM Complete!
REM ============================================================
echo.
echo ============================================================
echo    DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo    Files created in: %APP_DIR%
echo.
echo    START_ALL.bat    - Start everything (recommended)
echo    START_SERVER.bat - Start server only
echo    START_NGROK.bat  - Start ngrok only
echo    STOP_ALL.bat     - Stop everything
echo.
echo ============================================================
echo    TO START THE TOOL:
echo ============================================================
echo.
echo    1. Double-click START_ALL.bat
echo    2. Two windows will open (server + ngrok)
echo    3. Access at: https://%NGROK_DOMAIN%
echo.
echo ============================================================
echo.
set /p LAUNCH="Start the tool now? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    echo.
    echo Starting...
    start "" "%APP_DIR%\START_ALL.bat"
)
echo.
pause
