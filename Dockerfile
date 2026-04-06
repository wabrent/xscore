FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY backend/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь бэкенд
COPY backend/ .

# Создаем директорию для базы данных
RUN mkdir -p /app/data

EXPOSE 8000

# Инициализируем БД и запускаем сервер
CMD ["sh", "-c", "python -c \"from app.database import engine, Base; from app.models import post, scheduled_post, crypto_trend, analytics_data; Base.metadata.create_all(bind=engine)\" && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
