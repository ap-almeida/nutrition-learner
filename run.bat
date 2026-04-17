@echo off
:: Nutrition Chatbot — Windows launcher
setlocal

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

:: Create venv if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Python not found. Install Python 3.11+ from https://python.org
        pause
        exit /b 1
    )
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install/upgrade dependencies silently
pip install -q -r requirements.txt

:: Copy .env.example to .env if .env doesn't exist
if not exist ".env" (
    copy .env.example .env >nul
    echo.
    echo First run: edit .env and set your OPENAI_API_KEY, then run this script again.
    echo    notepad .env
    echo.
    pause
    exit /b 1
)

:: Run the chatbot
python chat.py

pause
