@echo off
REM ===============================================================
REM Amazon Audit Tool - Stop All Processes
REM ===============================================================

title Amazon Audit Tool - Stopping

echo.
echo ============================================================
echo    STOPPING AMAZON AUDIT TOOL...
echo ============================================================
echo.

echo [1/2] Stopping Python server...
taskkill /f /im python.exe 2>nul
if errorlevel 1 (
    echo    [INFO] No Python process found
) else (
    echo    [OK] Python server stopped
)

echo.
echo [2/2] Stopping ngrok...
taskkill /f /im ngrok.exe 2>nul
if errorlevel 1 (
    echo    [INFO] No ngrok process found
) else (
    echo    [OK] ngrok stopped
)

echo.
echo ============================================================
echo    ALL PROCESSES STOPPED!
echo ============================================================
echo.
echo    To restart, run START.bat
echo.
timeout /t 3
