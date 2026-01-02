@echo off
REM Quick script to activate virtual environment (Windows)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Virtual environment activated!
echo Python location:
where python
echo.
echo Installed packages:
pip list
echo.
echo To run the demo, use: streamlit run app.py
