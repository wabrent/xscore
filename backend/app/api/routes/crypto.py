from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ...services.crypto_service import CryptoService
from ...database import SessionLocal
from ...models.crypto_trend import CryptoTrend

router = APIRouter()
crypto_service = CryptoService()

@router.get("/top-coins")
async def get_top_coins(limit: int = Query(20, ge=1, le=100)):
    """Получение топ крипто-монет."""
    coins = await crypto_service.get_top_coins(limit)
    return {"coins": coins, "count": len(coins)}

@router.get("/trending")
async def get_trending_coins():
    """Получение трендовых крипто-монет."""
    coins = await crypto_service.get_trending_coins()
    return {"trending": coins, "count": len(coins)}

@router.get("/global")
async def get_global_data():
    """Получение глобальных данных рынка."""
    data = await crypto_service.get_global_data()
    if not data:
        raise HTTPException(status_code=500, detail="Ошибка получения данных")
    return data

@router.get("/coin/{coin_id}")
async def get_coin_data(coin_id: str):
    """Получение данных конкретной монеты."""
    data = await crypto_service.get_coin_data(coin_id)
    if not data:
        raise HTTPException(status_code=404, detail="Монета не найдена")
    return data

@router.get("/coin/{coin_id}/chart")
async def get_coin_chart(coin_id: str, days: int = Query(7, ge=1, le=365)):
    """Получение графика цен монеты."""
    chart_data = await crypto_service.get_coin_market_chart(coin_id, days)
    return {"coin_id": coin_id, "days": days, "data": chart_data}

@router.post("/track")
async def track_crypto_keywords(keywords: List[str]):
    """Отслеживание упоминаний крипто-ключевых слов в Twitter."""
    from ...services.twitter_service import TwitterService
    
    twitter_service = TwitterService()
    db = SessionLocal()
    
    try:
        trends = []
        for keyword in keywords:
            # Поиск упоминаний в Twitter
            tweets = twitter_service.search_tweets(f"${keyword} OR #{keyword}", max_results=50)
            mentions_count = len(tweets)
            
            # Получение данных о цене
            coin_data = await crypto_service.get_coin_data(keyword.lower())
            
            trend = CryptoTrend(
                token_symbol=keyword.upper(),
                token_name=coin_data.get("name", keyword) if coin_data else keyword,
                mentions_count=mentions_count,
                price_usd=coin_data.get("market_data", {}).get("current_price", {}).get("usd") if coin_data else None,
                price_change_24h=coin_data.get("market_data", {}).get("price_change_percentage_24h") if coin_data else None,
                market_cap=coin_data.get("market_data", {}).get("market_cap", {}).get("usd") if coin_data else None
            )
            
            db.add(trend)
            trends.append(trend)
        
        db.commit()
        
        return {
            "success": True,
            "tracked": len(trends),
            "trends": [{
                "token_symbol": t.token_symbol,
                "mentions_count": t.mentions_count,
                "price_usd": t.price_usd
            } for t in trends]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/trends")
async def get_tracked_trends(limit: int = Query(20, ge=1, le=100)):
    """Получение отслеживаемых трендов."""
    db = SessionLocal()
    try:
        trends = db.query(CryptoTrend).order_by(CryptoTrend.tracked_at.desc()).limit(limit).all()
        return {
            "trends": trends,
            "count": len(trends)
        }
    finally:
        db.close()
