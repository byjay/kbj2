@echo off
REM ========================================
REM KBJ2 R2 Cloud Storage Manager
REM ========================================

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

if "%1"=="" (
    goto :menu
)

if "%1"=="explore" (
    python main.py r2 explore
) else if "%1"=="upload" (
    python main.py r2 upload %2 %3 %4
) else if "%1"=="download" (
    python main.py r2 download %2 %3
) else if "%1"=="ls" (
    python main.py r2 ls %2
) else if "%1"=="rm" (
    python main.py r2 rm %2
) else if "%1"=="share" (
    python main.py r2 share %2 %3
) else (
    goto :menu
)

goto :eof

:menu
cls
echo ========================================
echo   KBJ2 R2 Cloud Storage Manager
echo ========================================
echo.
echo 1. Explore (File Explorer GUI)
echo 2. Upload File
echo 3. Upload Directory
echo 4. Download File
echo 5. List Files
echo 6. Delete File
echo 7. Generate Share URL
echo 8. Exit
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" (
    python main.py r2 explore
    pause
)
if "%choice%"=="2" (
    set /p filepath="Enter file path: "
    set /p r2key="Enter R2 key (optional): "
    if "!r2key!"=="" (
        python main.py r2 upload "!filepath!"
    ) else (
        python main.py r2 upload "!filepath!" --key "!r2key!"
    )
    pause
)
if "%choice%"=="3" (
    set /p dirpath="Enter directory path: "
    set /p prefix="Enter R2 prefix (optional): "
    if "!prefix!"=="" (
        python main.py r2 upload "!dirpath!"
    ) else (
        python main.py r2 upload "!dirpath!" --prefix "!prefix!"
    )
    pause
)
if "%choice%"=="4" (
    set /p r2key="Enter R2 file key: "
    set /p dest="Enter destination path (optional): "
    if "!dest!"=="" (
        python main.py r2 download "!r2key!"
    ) else (
        python main.py r2 download "!r2key!" --dest "!dest!"
    )
    pause
)
if "%choice%"=="5" (
    set /p prefix="Enter prefix (optional): "
    if "!prefix!"=="" (
        python main.py r2 ls
    ) else (
        python main.py r2 ls --prefix "!prefix!"
    )
    pause
)
if "%choice%"=="6" (
    set /p r2key="Enter R2 file key to delete: "
    python main.py r2 rm "!r2key!"
    pause
)
if "%choice%"=="7" (
    set /p r2key="Enter R2 file key: "
    set /p expires="Enter expiration in seconds (default 3600): "
    if "!expires!"=="" (
        python main.py r2 share "!r2key!"
    ) else (
        python main.py r2 share "!r2key!" --expires !expires!
    )
    pause
)
if "%choice%"=="8" (
    exit /b 0
)

goto :menu
