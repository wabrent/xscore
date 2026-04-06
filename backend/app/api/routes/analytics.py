from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from ...database import SessionLocal, get_db
from ...services.twitter_service import TwitterService
from ...services.crypto_service import CryptoService

router = APIRouter()

@router.get("/overview")
async def get_analytics_overview():
    """Общая аналитика."""
    twitter_service = TwitterService()
    crypto_service = CryptoService()
    
    # Получение глобальных данных рынка
    global_data = await crypto_service.get_global_data()
    
    # Топ монеты
    top_coins = await crypto_service.get_top_coins(limit=10)
    
    # Трендовые монеты
    trending = await crypto_service.get_trending_coins()
    
    return {
        "market_overview": global_data,
        "top_coins": top_coins[:5],
        "trending": trending[:5],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/posts")
async def get_posts_analytics():
    """Аналитика по постам."""
    from ...models.post import Post, PostStatus
    
    db = SessionLocal()
    try:
        total_posts = db.query(Post).count()
        published_posts = db.query(Post).filter(Post.status == PostStatus.PUBLISHED).count()
        scheduled_posts = db.query(Post).filter(Post.status == PostStatus.SCHEDULED).count()
        failed_posts = db.query(Post).filter(Post.status == PostStatus.FAILED).count()
        
        # Посты за последние 7 дней
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_posts = db.query(Post).filter(Post.created_at >= seven_days_ago).count()
        
        return {
            "total_posts": total_posts,
            "published_posts": published_posts,
            "scheduled_posts": scheduled_posts,
            "failed_posts": failed_posts,
            "recent_posts_7d": recent_posts
        }
    finally:
        db.close()

@router.get("/engagement")
async def get_engagement_metrics():
    """Метрики вовлеченности."""
    from ...models.post import Post, PostStatus
    
    db = SessionLocal()
    try:
        published_posts = db.query(Post).filter(
            Post.status == PostStatus.PUBLISHED,
            Post.tweet_id.isnot(None)
        ).all()
        
        engagement_data = []
        twitter_service = TwitterService()
        
        for post in published_posts[:10]:  # Анализируем последние 10 постов
            metrics = twitter_service.get_tweet_metrics(post.tweet_id)
            if metrics and metrics.get("metrics"):
                engagement_data.append({
                    "post_id": post.id,
                    "tweet_id": post.tweet_id,
                    "content": post.content[:100] + "..." if len(post.content) > 100 else post.content,
                    "published_at": post.published_at.isoformat() if post.published_at else None,
                    "metrics": metrics["metrics"]
                })
        
        return {
            "engagement_data": engagement_data,
            "total_analyzed": len(engagement_data)
        }
    finally:
        db.close()

@router.get("/crypto-trends")
async def get_crypto_trends_analytics():
    """Аналитика крипто-трендов."""
    from ...models.crypto_trend import CryptoTrend
    
    db = SessionLocal()
    try:
        # Топ по упоминаниям
        top_mentions = db.query(CryptoTrend).order_by(
            CryptoTrend.mentions_count.desc()
        ).limit(10).all()
        
        # Топ по изменению цены
        top_price_change = db.query(CryptoTrend).filter(
            CryptoTrend.price_change_24h.isnot(None)
        ).order_by(
            CryptoTrend.price_change_24h.desc()
        ).limit(10).all()
        
        # Средний сентимент по токенам
        sentiment_by_token = {}
        for trend in top_mentions:
            if trend.sentiment_score is not None:
                sentiment_by_token[trend.token_symbol] = trend.sentiment_score
        
        return {
            "top_mentions": top_mentions,
            "top_price_change": top_price_change,
            "sentiment_analysis": sentiment_by_token
        }
    finally:
        db.close()

@router.get("/timeline")
async def get_timeline_analytics(days: int = Query(30, ge=1, le=90)):
    """Аналитика по временной шкале."""
    from ...models.post import Post, PostStatus
    
    db = SessionLocal()
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Посты по дням
        posts_by_day = db.query(Post).filter(Post.created_at >= start_date).all()
        
        # Группировка по дням
        posts_data = {}
        for post in posts_by_day:
            day_key = post.created_at.strftime("%Y-%m-%d")
            if day_key not in posts_data:
                posts_data[day_key] = {"total": 0, "published": 0, "failed": 0}
            
            posts_data[day_key]["total"] += 1
            if post.status == PostStatus.PUBLISHED:
                posts_data[day_key]["published"] += 1
            elif post.status == PostStatus.FAILED:
                posts_data[day_key]["failed"] += 1
        
        return {
            "days": days,
            "posts_by_day": posts_data
        }
    finally:
        db.close()
