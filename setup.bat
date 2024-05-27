@echo off
REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python before running this script.
    exit /b 1
)

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install the required packages
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Please make sure it exists in the project directory.
    exit /b 1
)

echo Virtual environment setup is complete and activated.
echo To deactivate the virtual environment, run `deactivate`.
