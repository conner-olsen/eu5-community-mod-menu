@echo off
setlocal

REM CMM Settings Tool Launcher
REM Installs all dependencies automatically and launches the tool.

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
%PYTHON% -m pipx --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pipx...
    %PYTHON% -m pip install --user pipx >nul 2>&1
    if %errorlevel% neq 0 (
        %PYTHON% -m pip install pipx >nul 2>&1
        if %errorlevel% neq 0 (
            echo ERROR: Failed to install pipx.
            pause
            exit /b 1
        )
    )
)

REM Run the CMM Settings Tool
echo Starting CMM Settings Tool...
%PYTHON% -m pipx run --spec "git+https://github.com/conner-olsen/eu5-community-mod-menu#subdirectory=tools/cmm-settings-tool" cmm-settings-tool %*

REM Clean up
del "%~f0" >nul 2>&1
