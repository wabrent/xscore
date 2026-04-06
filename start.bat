@echo off
echo ========================================
echo  Запуск Crypto Twitter Tool
echo ========================================
echo.

echo [1/2] Запуск Backend...
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak > nul

echo [2/2] Запуск Frontend...
start cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo  Приложение запускается...
echo ========================================
echo.
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
pause
