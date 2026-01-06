@echo off
REM ===============================================================
REM Verify Repository Completeness
REM Check if all necessary files are present
REM ===============================================================

title Repository Verification

echo.
echo ============================================================
echo    REPOSITORY VERIFICATION
echo ============================================================
echo.

set MISSING_FILES=0

REM Check main files
echo [INFO] Checking main files...
if not exist "main_linux.py" (
    echo [ERROR] Missing: main_linux.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] main_linux.py
)

if not exist "requirements.txt" (
    echo [ERROR] Missing: requirements.txt
    set /a MISSING_FILES+=1
) else (
    echo [OK] requirements.txt
)

if not exist "SETUP.bat" (
    echo [ERROR] Missing: SETUP.bat
    set /a MISSING_FILES+=1
) else (
    echo [OK] SETUP.bat
)

echo.

REM Check audit-new-exe directory
echo [INFO] Checking audit-new-exe directory...
if not exist "audit-new-exe\runner_linux.py" (
    echo [ERROR] Missing: audit-new-exe\runner_linux.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] audit-new-exe\runner_linux.py
)

echo.

REM Check features directory
echo [INFO] Checking features directory...
if not exist "features\entry_point.py" (
    echo [ERROR] Missing: features\entry_point.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] features\entry_point.py
)

echo.

REM Check utils directory
echo [INFO] Checking utils directory...
if not exist "utils\proxy_manager.py" (
    echo [ERROR] Missing: utils\proxy_manager.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] utils\proxy_manager.py
)

if not exist "utils\read_file.py" (
    echo [ERROR] Missing: utils\read_file.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] utils\read_file.py
)

if not exist "utils\save_file.py" (
    echo [ERROR] Missing: utils\save_file.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] utils\save_file.py
)

echo.

REM Check traffic-generator directory
echo [INFO] Checking traffic-generator directory...
if not exist "traffic-generator\traffic_simulator.py" (
    echo [ERROR] Missing: traffic-generator\traffic_simulator.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] traffic-generator\traffic_simulator.py
)

if not exist "traffic-generator\gui_app.py" (
    echo [ERROR] Missing: traffic-generator\gui_app.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] traffic-generator\gui_app.py
)

echo.

REM Check installation scripts
echo [INFO] Checking installation scripts...
if not exist "INSTALL_ON_NEW_PC.bat" (
    echo [ERROR] Missing: INSTALL_ON_NEW_PC.bat
    set /a MISSING_FILES+=1
) else (
    echo [OK] INSTALL_ON_NEW_PC.bat
)

if not exist "DOWNLOAD_AND_INSTALL.bat" (
    echo [ERROR] Missing: DOWNLOAD_AND_INSTALL.bat
    set /a MISSING_FILES+=1
) else (
    echo [OK] DOWNLOAD_AND_INSTALL.bat
)

if not exist "UPDATE_TOOL.bat" (
    echo [ERROR] Missing: UPDATE_TOOL.bat
    set /a MISSING_FILES+=1
) else (
    echo [OK] UPDATE_TOOL.bat
)

echo.

REM Check documentation
echo [INFO] Checking documentation...
if not exist "README.md" (
    echo [ERROR] Missing: README.md
    set /a MISSING_FILES+=1
) else (
    echo [OK] README.md
)

if not exist "DEPLOYMENT_GUIDE.md" (
    echo [ERROR] Missing: DEPLOYMENT_GUIDE.md
    set /a MISSING_FILES+=1
) else (
    echo [OK] DEPLOYMENT_GUIDE.md
)

if not exist "DISTRIBUTION_INSTRUCTIONS.md" (
    echo [ERROR] Missing: DISTRIBUTION_INSTRUCTIONS.md
    set /a MISSING_FILES+=1
) else (
    echo [OK] DISTRIBUTION_INSTRUCTIONS.md
)

echo.

REM Final result
echo ============================================================
if %MISSING_FILES% EQU 0 (
    echo    ✅ REPOSITORY VERIFICATION PASSED!
    echo ============================================================
    echo.
    echo All necessary files are present.
    echo Repository is ready for distribution.
    echo.
    echo NEXT STEPS:
    echo 1. Test installation with SETUP.bat
    echo 2. Share repository URL with users
    echo 3. Provide DOWNLOAD_AND_INSTALL.bat for easy setup
    echo.
    echo Repository URL: https://github.com/ajcoder326/amazonscarping-tool.git
) else (
    echo    ❌ REPOSITORY VERIFICATION FAILED!
    echo ============================================================
    echo.
    echo Missing %MISSING_FILES% file(s).
    echo Please ensure all files are committed and pushed.
)

echo.
pause