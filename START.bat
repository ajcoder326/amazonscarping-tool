@echo off
REM ===============================================================
REM Amazon Audit Tool - Quick Start
REM Run this after deployment to start the tool
REM ===============================================================

title Amazon Audit Tool

echo.
echo ============================================================
echo    AMAZON AUDIT TOOL - Starting...
echo ============================================================
echo.

REM Get the directory where this bat file is located
set APP_DIR=%~dp0
cd /d "%APP_DIR%"

REM Check if deployment was done
if not exist "%APP_DIR%\venv" (
    echo.
    echo ============================================================
    echo    ERROR: DEPLOYMENT NOT DONE!
    echo ============================================================
    echo.
    echo Please run DEPLOY.bat first to set up the tool.
    echo.
    pause
    exit /b 1
)

if not exist "%APP_DIR%\tools\ngrok.exe" (
    echo.
    echo ============================================================
    echo    ERROR: NGROK NOT FOUND!
    echo ============================================================
    echo.
    echo Please run DEPLOY.bat first to set up ngrok.
    echo.
    pause
    exit /b 1
)

echo [1/2] Starting Flask server...
start "Audit Tool Server" cmd /k "cd /d "%APP_DIR%" && call venv\Scripts\activate.bat && set PYTHONPATH=%APP_DIR% && echo. && echo ============================================ && echo    Amazon Audit Tool - Server Running && echo ============================================ && echo. && echo Server starting on port 5000... && echo. && python -m waitress --host=0.0.0.0 --port=5000 --threads=8 web_app.app:app"

echo.
echo [INFO] Waiting for server to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting ngrok tunnel...

REM Check if domain is configured
set NGROK_DOMAIN=
for /f "tokens=*" %%a in ('"%APP_DIR%\tools\ngrok.exe" config check 2^>^&1 ^| findstr "domain"') do set NGROK_DOMAIN=%%a

start "ngrok Tunnel" cmd /k ""%APP_DIR%\tools\ngrok.exe" http 5000"

echo.
echo ============================================================
echo    READY!
echo ============================================================
echo.
echo    Two windows have opened:
echo       1. Server window - Shows request logs
echo       2. ngrok window  - Shows your public URL
echo.
echo    Look at the ngrok window to find your URL!
echo    It will look like: https://xxxx-xx-xx-xx-xx.ngrok-free.dev
echo.
echo    Share this URL with your users!
echo.
echo ============================================================
echo.
echo    To STOP: Close both windows or run STOP.bat
echo.
echo ============================================================
echo.
pause
