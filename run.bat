@echo off
setlocal enabledelayedexpansion

set venv_folder=env
set startup_file=src\main.py
set default_code=# your code here

REM Check if Python is installed
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed on this system.
    exit /b
)

echo [INFO] Checking virtual environment...

REM Check if venv is installed
python -c "import venv" > nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing venv...
    python -m ensurepip --upgrade
    python -m pip install virtualenv
)

REM Check if the venv folder exists
if not exist %venv_folder% (
    echo [INFO] Creating virtual environment...
    python -m venv %venv_folder%
    echo [INFO] Virtual environment created successfully.
)

REM Activate the virtual environment
call %venv_folder%\Scripts\activate.bat

REM Check if the src/main.py file exists
if not exist %startup_file% (
    echo [INFO] src/main.py not found. Creating directory and default main.py file...
    mkdir src
    echo. >> %startup_file%
    echo %default_code% >> %startup_file%
    echo [INFO] src/main.py created successfully.
)

echo [INFO] Running %startup_file%...

REM Run the startup file from the virtual environment
python %startup_file%

REM Deactivate the virtual environment
deactivate

echo [INFO] Project execution completed. DONE.

endlocal
