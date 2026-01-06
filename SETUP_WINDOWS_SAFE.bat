@echo off
REM ===============================================================
REM Amazon Scraping Tool - Windows Safe Setup Script
REM Handles C++ compiler issues by using pre-compiled wheels
REM ===============================================================

setlocal enabledelayedexpansion
title Amazon Scraping Tool - Windows Safe Setup

echo.
echo ============================================================
echo    AMAZON SCRAPING TOOL - WINDOWS SAFE SETUP
echo ============================================================
echo.
echo This script uses pre-compiled packages to avoid C++ compiler issues.
echo.
echo This script will automatically:
echo    1. Check Python installation
echo    2. Create virtual environment
echo    3. Install compatible packages (no compilation needed)
echo    4. Install Playwright browsers
echo    5. Create necessary directories
echo    6. Configure startup scripts
echo    7. Test installation
echo.
echo ============================================================
echo.
pause

REM Get the directory where this bat file is located
set TOOL_DIR=%~dp0
cd /d "%TOOL_DIR%"
set TOOL_DIR=%CD%

echo.
echo [INFO] Tool directory: %TOOL_DIR%
echo.

REM ============================================================
REM Step 1: Check Python Installation
REM ============================================================
echo ============================================================
echo [STEP 1/8] Checking Python installation...
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo    ERROR: PYTHON NOT FOUND!
    echo ============================================================
    echo.
    echo Please install Python 3.9 to 3.11 (recommended):
    echo    1. Go to: https://python.org/downloads
    echo    2. Download Python 3.11.x (AVOID 3.12+ for compatibility)
    echo    3. Run installer
    echo    4. IMPORTANT: Check "Add Python to PATH"
    echo    5. Click "Install Now"
    echo    6. Restart this script
    echo.
    echo ============================================================
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo    [OK] Python %PYTHON_VER% found!

REM Check Python version (recommend 3.9-3.11)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VER%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo    [ERROR] Python version too old. Need 3.9+
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 9 (
    echo    [WARNING] Python version is old. Recommend 3.9-3.11 for best compatibility
)

if %MAJOR% EQU 3 if %MINOR% GTR 11 (
    echo    [WARNING] Python 3.12+ may have compatibility issues. Recommend 3.9-3.11
)

echo    [OK] Python version is acceptable!
echo.

REM ============================================================
REM Step 2: Create Virtual Environment
REM ============================================================
echo ============================================================
echo [STEP 2/8] Creating Python virtual environment...
echo ============================================================
echo.

if exist "%TOOL_DIR%\venv" (
    echo    [INFO] Removing existing virtual environment...
    rmdir /s /q "%TOOL_DIR%\venv"
)

echo    [INFO] Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo    [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

echo    [OK] Virtual environment created!
echo.

REM ============================================================
REM Step 3: Activate Virtual Environment
REM ============================================================
echo ============================================================
echo [STEP 3/8] Activating virtual environment...
echo ============================================================
echo.

call "%TOOL_DIR%\venv\Scripts\activate.bat"
if errorlevel 1 (
    echo    [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

echo    [OK] Virtual environment activated!
echo.

REM ============================================================
REM Step 4: Upgrade pip
REM ============================================================
echo ============================================================
echo [STEP 4/8] Upgrading pip...
echo ============================================================
echo.

python -m pip install --upgrade pip
echo    [OK] Pip upgraded!
echo.

REM ============================================================
REM Step 5: Install Compatible Packages
REM ============================================================
echo ============================================================
echo [STEP 5/8] Installing compatible Python packages...
echo ============================================================
echo.

echo    [INFO] Installing packages with pre-compiled wheels only...
echo    [INFO] This avoids C++ compiler requirements...
echo.

REM Install core packages individually with specific versions
echo    [INFO] Installing numpy (compatible version)...
python -m pip install --only-binary=all "numpy>=1.21.0,<2.0.0"
if errorlevel 1 (
    echo    [ERROR] Failed to install numpy!
    echo    [INFO] Your system may need Visual Studio Build Tools
    echo    [INFO] Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    pause
    exit /b 1
)

echo    [INFO] Installing pandas (compatible version)...
python -m pip install --only-binary=all "pandas>=1.5.0,<2.0.0"

echo    [INFO] Installing openpyxl...
python -m pip install --only-binary=all openpyxl==3.1.2

echo    [INFO] Installing aiofiles...
python -m pip install --only-binary=all aiofiles==23.2.1

echo    [INFO] Installing requests...
python -m pip install --only-binary=all requests==2.31.0

echo    [INFO] Installing playwright...
python -m pip install playwright==1.40.0

echo    [INFO] Installing additional packages...
python -m pip install --only-binary=all pyee==11.1.0 typing_extensions==4.8.0 setuptools packaging

echo    [INFO] Installing optional packages...
python -m pip install playwright-stealth
if errorlevel 1 (
    echo    [WARNING] playwright-stealth failed to install (optional)
)

python -m pip install PyQt5
if errorlevel 1 (
    echo    [WARNING] PyQt5 failed to install (GUI will not work)
)

echo    [OK] Core packages installed successfully!
echo.

REM ============================================================
REM Step 6: Install Playwright Browsers
REM ============================================================
echo ============================================================
echo [STEP 6/8] Installing Playwright browsers...
echo ============================================================
echo.

echo    [INFO] This may take a few minutes...
python -m playwright install chromium
if errorlevel 1 (
    echo    [ERROR] Failed to install Playwright browsers!
    pause
    exit /b 1
)

echo    [OK] Playwright browsers installed!
echo.

REM ============================================================
REM Step 7: Create Directories
REM ============================================================
echo ============================================================
echo [STEP 7/8] Creating necessary directories...
echo ============================================================
echo.

REM Create output directory in user's Documents
set OUTPUT_DIR=%USERPROFILE%\Documents\Audited_files
if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
    echo    [OK] Created output directory: %OUTPUT_DIR%
)

REM Create cookies directory if it doesn't exist
if not exist "%TOOL_DIR%\cookies" (
    mkdir "%TOOL_DIR%\cookies"
    echo    [OK] Created cookies directory
)

REM Create sample cookies file if it doesn't exist
if not exist "%TOOL_DIR%\cookies\amazon_cookies.json" (
    echo [] > "%TOOL_DIR%\cookies\amazon_cookies.json"
    echo    [OK] Created sample cookies file
)

echo.

REM ============================================================
REM Step 8: Test Installation
REM ============================================================
echo ============================================================
echo [STEP 8/8] Testing installation...
echo ============================================================
echo.

echo    [INFO] Testing Python imports...
python -c "import sys; print(f'Python {sys.version}')"
python -c "import numpy; print(f'NumPy {numpy.__version__}')"
python -c "import pandas; print(f'Pandas {pandas.__version__}')"
python -c "import playwright; print('Playwright OK')"
python -c "import asyncio; print('AsyncIO OK')"

if errorlevel 1 (
    echo    [ERROR] Import test failed!
    pause
    exit /b 1
)

echo    [INFO] Testing Playwright browser...
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); browser.close(); p.stop(); print('Browser test successful!')"
if errorlevel 1 (
    echo    [ERROR] Browser test failed!
    pause
    exit /b 1
)

echo    [OK] All tests passed!
echo.

REM ============================================================
REM Create Quick Start Scripts
REM ============================================================
echo ============================================================
echo [INFO] Creating quick start scripts...
echo ============================================================
echo.

REM Create run_audit.bat
echo @echo off > run_audit.bat
echo cd /d "%TOOL_DIR%" >> run_audit.bat
echo call venv\Scripts\activate.bat >> run_audit.bat
echo set PYTHONPATH=%TOOL_DIR% >> run_audit.bat
echo echo. >> run_audit.bat
echo echo ============================================================ >> run_audit.bat
echo echo    AMAZON AUDIT TOOL - BATCH PROCESSOR >> run_audit.bat
echo echo ============================================================ >> run_audit.bat
echo echo. >> run_audit.bat
echo set /p ASIN_FILE="Enter path to your ASIN file (Excel/CSV): " >> run_audit.bat
echo if not exist "%%ASIN_FILE%%" ( >> run_audit.bat
echo     echo [ERROR] File not found: %%ASIN_FILE%% >> run_audit.bat
echo     pause >> run_audit.bat
echo     exit /b 1 >> run_audit.bat
echo ^) >> run_audit.bat
echo echo. >> run_audit.bat
echo echo [INFO] Starting audit process... >> run_audit.bat
echo python audit-new-exe\runner_linux.py -file "%%ASIN_FILE%%" -batch 5000 -wait 600 >> run_audit.bat
echo pause >> run_audit.bat

REM Create run_traffic_gui.bat
echo @echo off > run_traffic_gui.bat
echo cd /d "%TOOL_DIR%\traffic-generator" >> run_traffic_gui.bat
echo call ..\venv\Scripts\activate.bat >> run_traffic_gui.bat
echo set PYTHONPATH=%TOOL_DIR% >> run_traffic_gui.bat
echo echo. >> run_traffic_gui.bat
echo echo ============================================================ >> run_traffic_gui.bat
echo echo    AMAZON TRAFFIC GENERATOR - GUI MODE >> run_traffic_gui.bat
echo echo ============================================================ >> run_traffic_gui.bat
echo echo. >> run_traffic_gui.bat
echo python gui_app.py >> run_traffic_gui.bat
echo pause >> run_traffic_gui.bat

REM Create test_setup.bat
echo @echo off > test_setup.bat
echo cd /d "%TOOL_DIR%" >> test_setup.bat
echo call venv\Scripts\activate.bat >> test_setup.bat
echo set PYTHONPATH=%TOOL_DIR% >> test_setup.bat
echo echo. >> test_setup.bat
echo echo ============================================================ >> test_setup.bat
echo echo    TESTING INSTALLATION >> test_setup.bat
echo echo ============================================================ >> test_setup.bat
echo echo. >> test_setup.bat
echo echo [INFO] Testing cookies... >> test_setup.bat
echo python test_cookies.py >> test_setup.bat
echo echo. >> test_setup.bat
echo echo [INFO] Testing proxy (if configured)... >> test_setup.bat
echo python test_proxy.py >> test_setup.bat
echo echo. >> test_setup.bat
echo echo [OK] All tests completed! >> test_setup.bat
echo pause >> test_setup.bat

echo    [OK] Quick start scripts created!
echo.

REM ============================================================
REM Final Success Message
REM ============================================================
echo ============================================================
echo    SETUP COMPLETED SUCCESSFULLY! 🎉
echo ============================================================
echo.
echo Your Amazon Scraping Tool is now ready to use!
echo.
echo INSTALLED VERSIONS:
for /f "tokens=*" %%i in ('python -c "import numpy, pandas, playwright; print(f'NumPy: {numpy.__version__}, Pandas: {pandas.__version__}, Playwright: {playwright.__version__}')"') do echo    %%i
echo.
echo QUICK START OPTIONS:
echo.
echo 1. AUDIT MODE (Extract product data):
echo    - Double-click: run_audit.bat
echo    - Follow prompts to select your ASIN file
echo.
echo 2. TRAFFIC GENERATOR (GUI):
echo    - Double-click: run_traffic_gui.bat
echo    - Use the graphical interface
echo.
echo 3. TEST INSTALLATION:
echo    - Double-click: test_setup.bat
echo    - Verify everything works correctly
echo.
echo NEXT STEPS:
echo 1. Prepare your ASIN file (Excel/CSV format)
echo 2. Export Amazon cookies (see COOKIES_GUIDE.md)
echo 3. Configure proxies (optional, see documentation)
echo 4. Run your first audit or traffic simulation!
echo.
echo DOCUMENTATION:
echo - README.md - Complete usage guide
echo - QUICK_START.txt - Quick reference
echo - traffic-generator/USER_GUIDE.md - GUI guide
echo.
echo ============================================================
echo.
echo Installation completed in: %TOOL_DIR%
echo Output directory: %OUTPUT_DIR%
echo.
echo Happy scraping! 🚀
echo.
pause