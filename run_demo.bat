@echo off
REM Dubai Mall Intelligent Concierge - Quick Start Script (Windows)

echo ====================================================
echo   Dubai Mall Intelligent Concierge Demo
echo   Powered by Claude 3.5 Sonnet
echo ====================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [3/4] Installing dependencies...
pip install -r requirements.txt -q
echo.

REM Check for API key
if "%DEEPSEEK_API_KEY%"=="" (
    echo [WARNING] DEEPSEEK_API_KEY not set!
    echo.
    echo Please set your API key:
    echo   1. Get API key from: https://platform.deepseek.com/
    echo   2. Set environment variable: set DEEPSEEK_API_KEY=sk-xxxxx
    echo   3. Or enter it in the app's sidebar settings
    echo.
)

REM Run Streamlit app
echo [4/4] Starting Streamlit app...
echo.
echo ====================================================
echo   App will open in your browser automatically
echo   Press Ctrl+C to stop the server
echo ====================================================
echo.

streamlit run app.py

pause
