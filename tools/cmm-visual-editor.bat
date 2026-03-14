@echo off
setlocal

REM CMM Visual Editor Launcher
REM Installs all dependencies automatically and launches the tool.

set CMM_SPEC=git+https://github.com/conner-olsen/eu5-community-mod-menu#subdirectory=tools/cmm-visual-editor
REM Find Python
set PYTHON=
where python >nul 2>&1 && set PYTHON=python
if not defined PYTHON (
    where py >nul 2>&1 && set PYTHON=py
)

REM Install Python if not found
if not defined PYTHON (
    echo Python not found. Installing...
    where winget >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Could not auto-install Python. winget is not available.
        echo Please install Python 3.9 or later from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    winget install Python.Python.3.13 --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Python.
        echo Please install Python 3.9 or later from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    REM Find Python after install
    where py >nul 2>&1 && set PYTHON=py
    if not defined PYTHON (
        for /f "delims=" %%i in ('dir /b /ad "%LOCALAPPDATA%\Programs\Python\Python3*" 2^>nul') do (
            if exist "%LOCALAPPDATA%\Programs\Python\%%i\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\%%i\python.exe"
        )
    )
    if not defined PYTHON (
        echo Python was installed successfully but the terminal needs to be restarted.
        echo Please close this window and run the script again.
        pause
        exit /b 0
    )
)

REM Install pipx if not available
"%PYTHON%" -m pipx --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pipx...
    "%PYTHON%" -m pip install --user pipx >nul 2>&1
    if %errorlevel% neq 0 (
        "%PYTHON%" -m pip install pipx >nul 2>&1
        if %errorlevel% neq 0 (
            echo ERROR: Failed to install pipx.
            pause
            exit /b 1
        )
    )
)

REM Check if this is a local (persistent) launcher or a temp download
REM Local launchers are NOT in %TEMP%, so they install via pipx for auto-update
echo "%~f0" | findstr /i /c:"%TEMP%" >nul 2>&1
if %errorlevel% equ 0 (
    REM Temp download - run directly via pipx run, then clean up
    echo Starting CMM Visual Editor...
    "%PYTHON%" -m pipx run --spec "%CMM_SPEC%" cmm-visual-editor
    del "%~f0" >nul 2>&1
) else (
    REM Local launcher - install/update via pipx, then run
    "%PYTHON%" -m pipx list --short 2>nul | findstr /b "cmm-visual-editor" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Checking for updates...
        "%PYTHON%" -m pipx reinstall cmm-visual-editor >nul 2>&1
    ) else (
        echo Installing CMM Visual Editor...
        "%PYTHON%" -m pipx install "%CMM_SPEC%" >nul 2>&1
        if %errorlevel% neq 0 (
            echo ERROR: Failed to install CMM Visual Editor.
            pause
            exit /b 1
        )
    )
    echo Starting CMM Visual Editor...
    cmm-visual-editor
)
