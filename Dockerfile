# Этап 1: Сборка фронтенда
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Этап 2: Бэкенд с обслуживанием фронтенда
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей Python
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копирование бэкенда
COPY backend/ ./

# Копирование собранного фронтенда
COPY --from=frontend-build /app/frontend/build /app/static

# Создание директории для БД
RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite:///./data/crypto_twitter.db

# Переменные окружения (заполняются при запуске)
ENV TWITTER_API_KEY=""
ENV TWITTER_API_SECRET=""
ENV TWITTER_ACCESS_TOKEN=""
ENV TWITTER_ACCESS_TOKEN_SECRET=""
ENV TWITTER_BEARER_TOKEN=""

EXPOSE 8000

# Запуск сервера
CMD ["sh", "-c", "python -c \"from app.database import engine, Base; from app.models import post, scheduled_post, crypto_trend, analytics_data; Base.metadata.create_all(bind=engine)\" && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
