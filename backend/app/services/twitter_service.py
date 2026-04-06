import tweepy
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from datetime import datetime

load_dotenv()

class TwitterService:
    """Сервис для работы с Twitter API v2."""
    
    def __init__(self):
        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # Авторизация клиента
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token,
            wait_on_rate_limit=True
        )
        
        # API v1.1 для некоторых функций
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        self.api = tweepy.API(auth)
    
    def post_tweet(self, text: str) -> Dict:
        """Публикация твита."""
        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            return {
                "success": True,
                "tweet_id": tweet_id,
                "message": "Твит успешно опубликован"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_timeline(self, user_id: str, max_results: int = 100) -> List[Dict]:
        """Получение таймлайна пользователя."""
        try:
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "context_annotations"]
            )
            return tweets.data or []
        except Exception as e:
            print(f"Error fetching timeline: {e}")
            return []
    
    def search_tweets(self, query: str, max_results: int = 100) -> List[Dict]:
        """Поиск твитов по запросу."""
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "author_id", "context_annotations"]
            )
            return tweets.data or []
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []
    
    def get_tweet_metrics(self, tweet_id: str) -> Optional[Dict]:
        """Получение метрик твита."""
        try:
            tweet = self.client.get_tweet(
                id=tweet_id,
                tweet_fields=["public_metrics", "created_at"]
            )
            if tweet.data:
                return {
                    "id": tweet.data.id,
                    "text": tweet.data.text,
                    "created_at": tweet.data.created_at,
                    "metrics": tweet.data.public_metrics
                }
            return None
        except Exception as e:
            print(f"Error fetching tweet metrics: {e}")
            return None
    
    def get_user_metrics(self, user_id: str) -> Optional[Dict]:
        """Получение метрик пользователя."""
        try:
            user = self.client.get_user(
                id=user_id,
                user_fields=["public_metrics", "created_at"]
            )
            if user.data:
                return {
                    "id": user.data.id,
                    "username": user.data.username,
                    "name": user.data.name,
                    "metrics": user.data.public_metrics
                }
            return None
        except Exception as e:
            print(f"Error fetching user metrics: {e}")
            return None
    
    def get_crypto_mentions(self, keywords: List[str], max_results: int = 100) -> List[Dict]:
        """Поиск упоминаний крипто-ключевых слов."""
        mentions = []
        for keyword in keywords:
            query = f"${keyword} OR #{keyword} OR {keyword} crypto"
            tweets = self.search_tweets(query, max_results)
            for tweet in tweets:
                mentions.append({
                    "keyword": keyword,
                    "tweet": tweet
                })
        return mentions
    
    def delete_tweet(self, tweet_id: str) -> Dict:
        """Удаление твита."""
        try:
            self.client.delete_tweet(id=tweet_id)
            return {
                "success": True,
                "message": "Твит успешно удален"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
