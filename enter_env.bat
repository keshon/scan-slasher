@echo off
setlocal enabledelayedexpansion

set venv_folder=env
set startup_file=src/main.py

REM Check if the venv folder exists
if not exist %venv_folder% (
    echo [ERROR] Virtual environment does not exist. Please execute the "run.bat" file to set up the environment.
    exit /b
)

REM Activate the virtual environment
call %venv_folder%\Scripts\activate.bat

echo [INFO] Entered local environment instance. You can now install additional packages or run the project with 'run' command.

REM Start an infinite loop to accept commands
:command_loop
set /p command="> "
if "%command%"=="run" (
    echo [INFO] Running %startup_file%...
    python %startup_file%
) else (
    if "%command%"=="exit" (
        goto :exit_loop
    ) else (
        %command%
    )
)
goto :command_loop

REM Exit the loop and deactivate the virtual environment
:exit_loop
echo [INFO] Exited local environment instance.
deactivate

endlocal