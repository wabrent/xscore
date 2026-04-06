@echo off
echo ========================================
echo  Crypto Twitter Tool - Установка
echo ========================================
echo.

echo [1/3] Настройка Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
cd ..
echo.

echo [2/3] Настройка Frontend...
cd frontend
call npm install
cd ..
echo.

echo ========================================
echo  Установка завершена!
echo ========================================
echo.
echo ВАЖНО: Заполните backend\.env вашими Twitter API credentials
echo Получить их можно на: https://developer.twitter.com/
echo.
echo Для запуска выполните: start.bat
echo.
pause
