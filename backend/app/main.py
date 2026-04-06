from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api.routes import twitter, crypto, posts, analytics
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Создание таблиц базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crypto Twitter Tool",
    description="Полноценный инструмент для работы с крипто-твиттером",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(twitter.router, prefix="/api/twitter", tags=["twitter"])
app.include_router(crypto.router, prefix="/api/crypto", tags=["crypto"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

# Планировщик задач
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    """Запуск планировщика при старте приложения."""
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Остановка планировщика при завершении приложения."""
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Crypto Twitter Tool API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
