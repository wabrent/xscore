from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from typing import Dict, Optional
from datetime import datetime
from ..services.twitter_service import TwitterService
from ..database import SessionLocal
from ..models.post import Post, PostStatus

class SchedulerService:
    """Сервис для управления планировщиком постов."""
    
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler
        self.twitter_service = TwitterService()
        self.jobs: Dict[str, str] = {}  # job_id -> post_id
    
    def schedule_post(self, post: Post) -> Optional[str]:
        """Планирование публикации поста."""
        if not post.scheduled_at or post.status != PostStatus.SCHEDULED:
            return None
        
        job_id = f"post_{post.id}"
        
        try:
            self.scheduler.add_job(
                self._publish_post,
                DateTrigger(run_date=post.scheduled_at),
                id=job_id,
                args=[post.id],
                replace_existing=True
            )
            self.jobs[job_id] = str(post.id)
            return job_id
        except Exception as e:
            print(f"Error scheduling post: {e}")
            return None
    
    def cancel_scheduled_post(self, job_id: str) -> bool:
        """Отмена запланированного поста."""
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]
            return True
        except Exception as e:
            print(f"Error canceling job: {e}")
            return False
    
    async def _publish_post(self, post_id: int):
        """Публикация поста (внутренний метод)."""
        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                print(f"Post {post_id} not found")
                return
            
            result = self.twitter_service.post_tweet(post.content)
            
            if result["success"]:
                post.status = PostStatus.PUBLISHED
                post.published_at = datetime.utcnow()
                post.tweet_id = result["tweet_id"]
            else:
                post.status = PostStatus.FAILED
                print(f"Failed to publish post {post_id}: {result['error']}")
            
            db.commit()
        except Exception as e:
            print(f"Error publishing post {post_id}: {e}")
            db.rollback()
        finally:
            db.close()
    
    def get_active_jobs(self) -> Dict[str, str]:
        """Получение активных задач."""
        return self.jobs.copy()
    
    def pause_job(self, job_id: str) -> bool:
        """Приостановка задачи."""
        try:
            self.scheduler.pause_job(job_id)
            return True
        except Exception as e:
            print(f"Error pausing job: {e}")
            return False
    
    def resume_job(self, job_id: str) -> bool:
        """Возобновление задачи."""
        try:
            self.scheduler.resume_job(job_id)
            return True
        except Exception as e:
            print(f"Error resuming job: {e}")
            return False
