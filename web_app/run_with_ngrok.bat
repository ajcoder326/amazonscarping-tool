@echo off
title Amazon Audit - Server + Ngrok
cd /d "%~dp0"
cd ..

echo ========================================
echo   Amazon ASIN Audit Tool
echo   Web Server + Ngrok Tunnel
echo ========================================
echo.

REM Check if ngrok is installed
ngrok version >nul 2>&1
if errorlevel 1 (
    echo ERROR: ngrok not found!
    echo.
    echo Please install ngrok:
    echo   1. Download from: https://ngrok.com/download
    echo   2. Extract ngrok.exe to a folder
    echo   3. Add to PATH or place in this folder
    echo   4. Run: ngrok config add-authtoken YOUR_TOKEN
    echo.
    pause
    exit /b 1
)

set PYTHONPATH=%cd%

echo Starting Flask server in background...
start "Flask Server" cmd /c "python web_app\app.py"

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting ngrok tunnel...
echo.
echo ========================================
echo   Share the ngrok URL with your users!
echo   They can upload ASIN files directly
echo ========================================
echo.

ngrok http 5000

pause
