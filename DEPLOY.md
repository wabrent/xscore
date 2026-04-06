# Render Deployment Guide

## Деплой на Render.com (бесплатно)

### 1. Подключение репозитория

1. Зайдите на https://render.com
2. Sign Up через GitHub
3. Нажмите **New +** → **Web Service**
4. Выберите репозиторий: `wabrent/xscore`

### 2. Настройка Web Service

Заполните:
- **Name:** `cryptocv`
- **Region:** выберите ближайший (например, Frankfurt)
- **Branch:** `master`
- **Root Directory:** оставьте пустым
- **Runtime:** `Docker`
- **Instance Type:** `Free`

### 3. Переменные окружения (Environment Variables)

В секции Environment Variables добавьте:

```
TWITTER_API_KEY=ваш_ключ
TWITTER_API_SECRET=ваш_ключ
TWITTER_ACCESS_TOKEN=ваш_ключ
TWITTER_ACCESS_TOKEN_SECRET=ваш_ключ
TWITTER_BEARER_TOKEN=ваш_ключ
```

### 4. Деплой

Нажмите **Create Web Service**

Render автоматически:
- Считает Dockerfile
- Соберет образ
- Задеплоит приложение

Получите URL вида: `https://cryptocv-xxxx.onrender.com`

---

## Альтернатива: Railway.app

1. Зайдите на https://railway.app
2. Connect GitHub
3. Выберите `wabrent/xscore`
4. Railway автоматически найдет Dockerfile
5. Добавьте переменные окружения
6. Деплой автоматический

---

## Альтернатива: Fly.io

```bash
# Установите flyctl
# https://fly.io/docs/hands-on/install-flyctl/

fly auth login
fly launch --name cryptocv
fly secrets set TWITTER_API_KEY=xxx TWITTER_API_SECRET=xxx ...
fly deploy
```

---

## Что делает приложение

После деплоя:
- Backend API доступен по адресу вашего деплоя
- API документация: `https://your-app.onrender.com/docs`
- Health check: `https://your-app.onrender.com/health`
