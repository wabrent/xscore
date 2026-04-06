from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, Base
from .api.routes import twitter, crypto, posts, analytics
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

# Создание таблиц базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crypto Twitter Tool",
    description="Полноценный инструмент для работы с крипто-твиттером",
    version="1.0.0"
)

# Обслуживание статических файлов (React build)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

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
    # Если есть статические файлы, отдаем index.html
    static_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"message": "Crypto Twitter Tool API", "version": "1.0.0"}

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # Catch-all маршрут для React роутинга
    static_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", full_path)
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return FileResponse(static_file)
    
    # Если файл не найден, отдаем index.html для клиентского роутинга
    index_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    return {"message": "Not Found"}, 404

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
