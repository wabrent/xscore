from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ...database import SessionLocal, get_db
from ...models.post import Post, PostStatus
from ...services.scheduler_service import SchedulerService

router = APIRouter()

class PostCreate(BaseModel):
    content: str
    scheduled_at: Optional[datetime] = None
    crypto_tags: Optional[List[str]] = None

class PostUpdate(BaseModel):
    content: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    crypto_tags: Optional[List[str]] = None

def get_scheduler():
    """Зависимость для получения планировщика."""
    from ...main import scheduler
    return SchedulerService(scheduler)

@router.post("/")
async def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    """Создание нового поста."""
    status = PostStatus.SCHEDULED if post_data.scheduled_at else PostStatus.DRAFT
    
    post = Post(
        content=post_data.content,
        status=status,
        scheduled_at=post_data.scheduled_at,
        crypto_tags=",".join(post_data.crypto_tags) if post_data.crypto_tags else None
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    result = {"success": True, "post": post}
    
    # Если пост запланирован, добавляем в планировщик
    if post.scheduled_at and post.status == PostStatus.SCHEDULED:
        scheduler = get_scheduler()
        job_id = scheduler.schedule_post(post)
        if job_id:
            result["job_id"] = job_id
    
    return result

@router.get("/")
async def get_posts(
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Получение списка постов."""
    query = db.query(Post)
    
    if status:
        query = query.filter(Post.status == status)
    
    posts = query.order_by(Post.created_at.desc()).limit(limit).all()
    return {"posts": posts, "count": len(posts)}

@router.get("/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Получение конкретного поста."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post

@router.put("/{post_id}")
async def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    """Обновление поста."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    if post_data.content is not None:
        post.content = post_data.content
    
    if post_data.scheduled_at is not None:
        post.scheduled_at = post_data.scheduled_at
        if post.status == PostStatus.DRAFT:
            post.status = PostStatus.SCHEDULED
    
    if post_data.crypto_tags is not None:
        post.crypto_tags = ",".join(post_data.crypto_tags)
    
    db.commit()
    db.refresh(post)
    
    # Перепланирование если нужно
    if post.scheduled_at and post.status == PostStatus.SCHEDULED:
        scheduler = get_scheduler()
        scheduler.schedule_post(post)
    
    return {"success": True, "post": post}

@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удаление поста."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    # Отмена запланированного поста
    if post.status == PostStatus.SCHEDULED:
        scheduler = get_scheduler()
        job_id = f"post_{post_id}"
        scheduler.cancel_scheduled_post(job_id)
    
    db.delete(post)
    db.commit()
    
    return {"success": True, "message": "Пост удален"}

@router.post("/{post_id}/publish")
async def publish_now(post_id: int, db: Session = Depends(get_db)):
    """Немедленная публикация поста."""
    from ...services.twitter_service import TwitterService
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    if post.status == PostStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Пост уже опубликован")
    
    twitter_service = TwitterService()
    result = twitter_service.post_tweet(post.content)
    
    if result["success"]:
        post.status = PostStatus.PUBLISHED
        post.published_at = datetime.utcnow()
        post.tweet_id = result["tweet_id"]
        db.commit()
        return {"success": True, "tweet_id": result["tweet_id"]}
    else:
        post.status = PostStatus.FAILED
        db.commit()
        raise HTTPException(status_code=400, detail=result.get("error", "Ошибка публикации"))

@router.post("/{post_id}/schedule")
async def schedule_post(post_id: int, scheduled_at: datetime, db: Session = Depends(get_db)):
    """Планирование поста."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    post.scheduled_at = scheduled_at
    post.status = PostStatus.SCHEDULED
    db.commit()
    
    scheduler = get_scheduler()
    job_id = scheduler.schedule_post(post)
    
    return {"success": True, "job_id": job_id}
