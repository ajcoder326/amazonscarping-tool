@echo off
title Amazon Audit Web Server
cd /d "%~dp0"
cd ..

echo ========================================
echo   Amazon ASIN Audit Tool - Web Server
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo [1/3] Setting up environment...
set PYTHONPATH=%cd%

echo [2/3] Installing dependencies (if needed)...
pip install flask werkzeug pandas openpyxl playwright aiofiles --quiet

echo [3/3] Starting web server...
echo.
echo ========================================
echo   Server will start on port 5000
echo   Local URL: http://localhost:5000
echo ========================================
echo.
echo To expose to internet, run in another terminal:
echo   ngrok http 5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python web_app\app.py

pause
