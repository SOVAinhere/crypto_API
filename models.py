from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
