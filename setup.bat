@echo off
echo ================================================
echo QuizBot Setup Script
echo ================================================
echo.

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 2: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 3: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo ✅ .env file created from .env.example
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your Google API key!
    echo    Get your API key from: https://makersuite.google.com/app/apikey
    echo.
) else (
    echo ✅ .env file already exists
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Google API key
echo 2. Run: python run_server.py
echo 3. Open frontend/index.html in your browser
echo.
pause
