from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from ...services.twitter_service import TwitterService
from ...services.crypto_service import CryptoService

router = APIRouter()
twitter_service = TwitterService()
crypto_service = CryptoService()

class TweetRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 100

@router.post("/tweet")
async def create_tweet(request: TweetRequest):
    """Публикация твита."""
    result = twitter_service.post_tweet(request.text)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Ошибка публикации"))
    return result

@router.get("/search")
async def search_tweets(query: str = Query(..., description="Поисковый запрос"), max_results: int = 100):
    """Поиск твитов."""
    tweets = twitter_service.search_tweets(query, max_results)
    return {"query": query, "count": len(tweets), "tweets": tweets}

@router.get("/user/{user_id}/timeline")
async def get_user_timeline(user_id: str, max_results: int = 100):
    """Получение таймлайна пользователя."""
    tweets = twitter_service.get_user_timeline(user_id, max_results)
    return {"user_id": user_id, "count": len(tweets), "tweets": tweets}

@router.get("/tweet/{tweet_id}/metrics")
async def get_tweet_metrics(tweet_id: str):
    """Получение метрик твита."""
    metrics = twitter_service.get_tweet_metrics(tweet_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Твит не найден")
    return metrics

@router.get("/user/{user_id}/metrics")
async def get_user_metrics(user_id: str):
    """Получение метрик пользователя."""
    metrics = twitter_service.get_user_metrics(user_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return metrics

@router.post("/crypto-mentions")
async def get_crypto_mentions(keywords: List[str], max_results: int = 100):
    """Поиск упоминаний крипто-ключевых слов."""
    mentions = twitter_service.get_crypto_mentions(keywords, max_results)
    
    # Анализ сентимента
    tweets_for_sentiment = [m["tweet"] for m in mentions]
    sentiment = await crypto_service.analyze_crypto_sentiment(tweets_for_sentiment)
    
    return {
        "mentions": mentions,
        "sentiment": sentiment,
        "total": len(mentions)
    }

@router.delete("/tweet/{tweet_id}")
async def delete_tweet(tweet_id: str):
    """Удаление твита."""
    result = twitter_service.delete_tweet(tweet_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Ошибка удаления"))
    return result
