@echo off
echo Starting Django Quiz Bot Frontend...
echo.
echo Make sure your FastAPI backend is running on http://localhost:8000
echo Django frontend will be available at http://localhost:8001
echo.

cd /d "%~dp0"

echo Running migrations...
python manage.py migrate

echo.
echo Starting Django development server...
python manage.py runserver 8001

pause
