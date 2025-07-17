@echo off
title Quiz Bot - Full Stack Launcher
color 0A

echo.
echo  ██████╗ ██╗   ██╗██╗███████╗    ██████╗  ██████╗ ████████╗
echo ██╔═══██╗██║   ██║██║╚══███╔╝    ██╔══██╗██╔═══██╗╚══██╔══╝
echo ██║   ██║██║   ██║██║  ███╔╝     ██████╔╝██║   ██║   ██║   
echo ██║▄▄ ██║██║   ██║██║ ███╔╝      ██╔══██╗██║   ██║   ██║   
echo ╚██████╔╝╚██████╔╝██║███████╗    ██████╔╝╚██████╔╝   ██║   
echo  ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
echo.
echo                    Django Frontend Launcher
echo ================================================================
echo.

cd /d "%~dp0"

echo [INFO] Checking FastAPI Backend...
echo [INFO] Make sure FastAPI backend is running on http://localhost:8000
echo.

echo [INFO] Starting Django Frontend Server...
echo.

cd django_frontend

echo [STEP 1] Running Django migrations...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Migration failed!
    pause
    exit /b 1
)

echo.
echo [STEP 2] Starting Django development server...
echo.
echo ================================================================
echo  🎉 Django Frontend starting on: http://localhost:8001
echo  🔧 FastAPI Backend should be on: http://localhost:8000
echo  📚 API Documentation: http://localhost:8000/docs
echo.
echo  💡 Make sure you have a .env file with GOOGLE_API_KEY
echo  ⚡ Press Ctrl+C to stop the server
echo ================================================================
echo.

python manage.py runserver 8001

echo.
echo [INFO] Django server stopped.
pause
