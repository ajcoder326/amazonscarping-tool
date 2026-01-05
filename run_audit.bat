@echo off
cd /d "f:\audit updated v1"
set PYTHONPATH=f:\audit updated v1

echo ========================================
echo Amazon Audit Script - Batch Mode
echo ========================================
echo.
echo Features:
echo  - Amazon Cookie Authentication
echo  - Batch Processing (5k per batch)
echo  - 10 Minute Cooldown Between Batches
echo  - Random Delays (2-4 seconds)
echo.

REM Change the file path below to your ASIN file
set ASIN_FILE=C:\Users\devco\Downloads\Bheemraj-437 asin-20-11-25.xlsx
echo File: %ASIN_FILE%
echo Batch Size: 5000 ASINs
echo Wait Time: 10 minutes between batches
echo.

"C:\Program Files\Python312\python.exe" "audit-new-exe\runner_linux.py" -file "%ASIN_FILE%" -batch 5000 -wait 600

pause
