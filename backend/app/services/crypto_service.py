import httpx
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from datetime import datetime

load_dotenv()

class CryptoService:
    """Сервис для работы с крипто-данными (CoinGecko API)."""
    
    def __init__(self):
        self.base_url = os.getenv("COINGECKO_API_URL", "https://api.coingecko.com/api/v3")
    
    async def get_top_coins(self, limit: int = 20) -> List[Dict]:
        """Получение топ крипто-монет по рыночной капитализации."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/coins/markets",
                    params={
                        "vs_currency": "usd",
                        "order": "market_cap_desc",
                        "per_page": limit,
                        "page": 1,
                        "sparkline": False,
                        "price_change_percentage": "24h"
                    }
                )
                return response.json()
        except Exception as e:
            print(f"Error fetching top coins: {e}")
            return []
    
    async def get_coin_data(self, coin_id: str) -> Optional[Dict]:
        """Получение данных конкретной монеты."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/coins/{coin_id}")
                return response.json()
        except Exception as e:
            print(f"Error fetching coin data: {e}")
            return None
    
    async def get_coin_market_chart(self, coin_id: str, days: int = 7) -> Dict:
        """Получение графика цен монеты."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/coins/{coin_id}/market_chart",
                    params={"vs_currency": "usd", "days": days}
                )
                return response.json()
        except Exception as e:
            print(f"Error fetching market chart: {e}")
            return {}
    
    async def get_trending_coins(self) -> List[Dict]:
        """Получение трендовых крипто-монет."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/search/trending")
                data = response.json()
                return data.get("coins", [])
        except Exception as e:
            print(f"Error fetching trending coins: {e}")
            return []
    
    async def get_global_data(self) -> Optional[Dict]:
        """Получение глобальных данных рынка."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/global")
                return response.json().get("data", {})
        except Exception as e:
            print(f"Error fetching global data: {e}")
            return None
    
    def extract_crypto_keywords(self, text: str) -> List[str]:
        """Извлечение крипто-ключевых слов из текста."""
        common_crypto = [
            "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "MATIC",
            "DOT", "AVAX", "SHIB", "DAI", "TRX", "LINK", "ATOM",
            "UNI", "LTC", "FTM", "NEAR", "APT", "ARB", "OP",
            "Bitcoin", "Ethereum", "Solana", "Cardano", "Polkadot",
            "crypto", "blockchain", "defi", "nft", "web3"
        ]
        
        text_upper = text.upper()
        found_keywords = [kw for kw in common_crypto if kw.upper() in text_upper]
        return found_keywords
    
    async def analyze_crypto_sentiment(self, tweets: List[Dict]) -> Dict[str, float]:
        """Анализ сентимента по крипто-твитам (базовый)."""
        positive_words = ["moon", "pump", "bullish", "gain", "profit", "buy", "hold", "hodl"]
        negative_words = ["dump", "crash", "bearish", "loss", "sell", "panic", "fud", "scam"]
        
        sentiment_scores = {}
        
        for tweet in tweets:
            text = tweet.get("text", "").lower()
            keywords = self.extract_crypto_keywords(text)
            
            for keyword in keywords:
                if keyword not in sentiment_scores:
                    sentiment_scores[keyword] = {"positive": 0, "negative": 0, "neutral": 0}
                
                for word in positive_words:
                    if word in text:
                        sentiment_scores[keyword]["positive"] += 1
                
                for word in negative_words:
                    if word in text:
                        sentiment_scores[keyword]["negative"] += 1
                
                if sentiment_scores[keyword]["positive"] == 0 and sentiment_scores[keyword]["negative"] == 0:
                    sentiment_scores[keyword]["neutral"] += 1
        
        # Расчет итогового сентимента
        result = {}
        for keyword, scores in sentiment_scores.items():
            total = scores["positive"] + scores["negative"] + scores["neutral"]
            if total > 0:
                result[keyword] = (scores["positive"] - scores["negative"]) / total
            else:
                result[keyword] = 0.0
        
        return result
