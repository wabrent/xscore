"""
Скрипт для инициализации базы данных и быстрого теста.
Запуск: python quick_test.py
"""
import sys
import os

# Добавляем путь к backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import engine, Base
from app.models import post, scheduled_post, crypto_trend, analytics_data

def init_db():
    """Создание всех таблиц в базе данных."""
    print("📦 Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ База данных успешно инициализирована!")
    print("📁 Файл БД: crypto_twitter.db")

if __name__ == "__main__":
    print("=" * 50)
    print("  Crypto Twitter Tool - Инициализация БД")
    print("=" * 50)
    print()
    
    try:
        init_db()
        print()
        print("=" * 50)
        print("  Готово! Теперь можно запустить приложение:")
        print("  1. Backend: cd backend && uvicorn app.main:app --reload")
        print("  2. Frontend: cd frontend && npm start")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("\nУбедитесь, что установлены все зависимости:")
        print("  cd backend && pip install -r requirements.txt")
        sys.exit(1)
