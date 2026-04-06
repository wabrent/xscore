# 🚀 Crypto Twitter Tool

Полноценный инструмент для работы с крипто-твиттером с веб-интерфейсом.

## Возможности

### 📊 Мониторинг крипто-трендов
- Отслеживание топ криптовалют по рыночной капитализации
- Мониторинг трендовых монет в реальном времени
- Анализ упоминаний крипто-токенов в Twitter
- Базовый анализ сентимента

### 📝 Планировщик постов
- Создание и редактирование постов
- Планирование публикации на определенное время
- Немедленная публикация
- Автоматическая публикация по расписанию
- Поддержка крипто-тегов

### 📈 Аналитика и дашборд
- Общая статистика постов
- Метрики вовлеченности (лайки, ретвиты, ответы)
- Графики активности по дням
- Анализ крипто-трендов
- Топ по упоминаниям и изменению цены

## Технологии

**Backend:**
- Python + FastAPI
- SQLAlchemy (SQLite)
- Tweepy (Twitter API v2)
- APScheduler
- HTTPX (для CoinGecko API)

**Frontend:**
- React
- React Bootstrap
- Recharts (графики)
- Moment.js
- Axios

## Установка

### 1. Клонирование репозитория

```bash
cd c:\Users\waabrent\Documents\trae_projects\twitter
```

### 2. Настройка Backend

```bash
cd backend

# Создание виртуального окружения
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt

# Копирование .env.example в .env и настройка credentials
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

**Важно:** Заполните `.env` вашими Twitter API credentials:
- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET
- TWITTER_BEARER_TOKEN

Получить их можно на: https://developer.twitter.com/

### 3. Настройка Frontend

```bash
cd frontend

# Установка зависимостей
npm install
```

## Запуск

### Запуск Backend

```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен по адресу: http://localhost:8000
API документация: http://localhost:8000/docs

### Запуск Frontend

```bash
cd frontend
npm start
```

Frontend будет доступен по адресу: http://localhost:3000

## Использование

### 1. Дашборд
- Общая статистика
- Топ крипто-монеты
- Трендовые монеты
- Распределение постов

### 2. Посты
- Создание новых постов
- Планирование публикации
- Редактирование существующих
- Немедленная публикация
- Удаление постов

### 3. Крипто-тренды
- Поиск твитов по крипто-ключевым словам
- Отслеживание упоминаний
- Просмотр топ и трендовых монет
- Анализ сентимента

### 4. Аналитика
- Статистика постов
- Метрики вовлеченности
- Графики активности
- Топ по упоминаниям и цене

## Структура проекта

```
twitter/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI приложение
│   │   ├── database.py          # Настройка БД
│   │   ├── api/
│   │   │   └── routes/         # API маршруты
│   │   ├── services/           # Бизнес-логика
│   │   └── models/             # Модели БД
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/        # React компоненты
│   │   ├── pages/             # Страницы
│   │   └── services/          # API сервисы
│   └── package.json
└── README.md
```

## API Endpoints

### Twitter
- `POST /api/twitter/tweet` - Публикация твита
- `GET /api/twitter/search?query=&max_results=` - Поиск твитов
- `POST /api/twitter/crypto-mentions` - Поиск крипто-упоминаний
- `DELETE /api/twitter/tweet/{tweet_id}` - Удаление твита

### Crypto
- `GET /api/crypto/top-coins?limit=` - Топ монеты
- `GET /api/crypto/trending` - Трендовые монеты
- `GET /api/crypto/global` - Глобальные данные рынка
- `GET /api/crypto/coin/{coin_id}` - Данные монеты
- `POST /api/crypto/track` - Отслеживание ключевых слов

### Posts
- `GET /api/posts/` - Список постов
- `POST /api/posts/` - Создание поста
- `PUT /api/posts/{post_id}` - Обновление поста
- `DELETE /api/posts/{post_id}` - Удаление поста
- `POST /api/posts/{post_id}/publish` - Публикация сейчас
- `POST /api/posts/{post_id}/schedule` - Планирование

### Analytics
- `GET /api/analytics/overview` - Общая аналитика
- `GET /api/analytics/posts` - Статистика постов
- `GET /api/analytics/engagement` - Метрики вовлеченности
- `GET /api/analytics/crypto-trends` - Аналитика крипто-трендов

## Безопасность

⚠️ **Никогда не коммитьте файл `.env`!**
⚠️ Храните API ключи в секрете

## Лицензия

MIT

## Поддержка

При возникновении проблем создавайте Issue в репозитории.
