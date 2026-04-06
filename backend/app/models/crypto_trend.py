from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from ..database import Base

class CryptoTrend(Base):
    __tablename__ = "crypto_trends"

    id = Column(Integer, primary_key=True, index=True)
    token_symbol = Column(String, nullable=False, index=True)
    token_name = Column(String, nullable=False)
    mentions_count = Column(Integer, default=0)
    sentiment_score = Column(Float, nullable=True)
    price_usd = Column(Float, nullable=True)
    price_change_24h = Column(Float, nullable=True)
    volume_24h = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    trend_score = Column(Float, nullable=True)
    tracked_at = Column(DateTime, server_default=func.now())
    source = Column(String, nullable=True)  # twitter, coingecko, etc.
