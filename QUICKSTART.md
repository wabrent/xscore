# 🚀 Быстрый старт

## Шаг 1: Получение Twitter API ключей

1. Перейдите на https://developer.twitter.com/
2. Войдите в аккаунт или создайте новый
3. Создайте новый Project и App
4. Получите следующие ключи:
   - API Key & Secret
   - Access Token & Secret
   - Bearer Token

**Важно:** Для полноценной работы нужен доступ к Twitter API v2 с правами на чтение и запись.

## Шаг 2: Установка приложения

### Вариант А: Автоматическая установка (Windows)

```bash
install.bat
```

### Вариант Б: Ручная установка

#### Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

#### Frontend:
```bash
cd frontend
npm install
```

## Шаг 3: Настройка .env файла

Откройте `backend\.env` и заполните вашими Twitter API ключами:

```env
TWITTER_API_KEY=ваш_api_key
TWITTER_API_SECRET=ваш_api_secret
TWITTER_ACCESS_TOKEN=ваш_access_token
TWITTER_ACCESS_TOKEN_SECRET=ваш_access_token_secret
TWITTER_BEARER_TOKEN=ваш_bearer_token
```

## Шаг 4: Инициализация базы данных

```bash
python quick_test.py
```

Или вручную:
```bash
cd backend
venv\Scripts\activate
python
>>> from app.database import engine, Base
>>> from app.models import post, scheduled_post, crypto_trend, analytics_data
>>> Base.metadata.create_all(bind=engine)
>>> exit()
```

## Шаг 5: Запуск приложения

### Вариант А: Использование start.bat (Windows)

```bash
start.bat
```

### Вариант Б: Ручной запуск

#### Терминал 1 - Backend:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Терминал 2 - Frontend:
```bash
cd frontend
npm start
```

## Шаг 6: Открытие приложения

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Документация:** http://localhost:8000/docs

## Возможные проблемы и решения

### Ошибка: "ModuleNotFoundError: No module named 'xxx'"

```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Ошибка: "Twitter API credentials invalid"

Проверьте файл `backend\.env` и убедитесь, что все ключи заполнены правильно.

### Ошибка: "Port 8000 already in use"

Измените порт в команде запуска:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Или остановите процесс, использующий порт 8000:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend не запускается

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## Использование приложения

### 1. Дашборд
- Просмотр общей статистики
- Топ криптовалют
- Трендовые монеты

### 2. Посты
- Создание новых твитов
- Планирование публикации
- Управление постами

### 3. Крипто-тренды
- Поиск твитов по крипто-ключевым словам
- Отслеживание упоминаний
- Анализ рынка

### 4. Аналитика
- Статистика постов
- Метрики вовлеченности
- Графики и диаграммы

## Дополнительная информация

- Документация API: http://localhost:8000/docs
- Исходный код backend: `backend/app/`
- Исходный код frontend: `frontend/src/`

## Поддержка

При возникновении проблем создавайте Issue в репозитории.
