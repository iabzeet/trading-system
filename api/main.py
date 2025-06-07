from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.sql import func
from api.celery_config import send_notification


app = FastAPI()
DATABASE_URL = "postgresql://abhijeet:abhijeet111@localhost/trading_system"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    side = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

class TradeCreate(BaseModel):
    ticker: str
    price: float
    quantity: int
    side: str

    @field_validator("price")
    def price_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Price must be non-negative")
        return v

    @field_validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v

    @field_validator("side")
    def side_must_be_valid(cls, v):
        if v not in ["buy", "sell"]:
            raise ValueError("Side must be 'buy' or 'sell'")
        return v
    
@app.post("/trades")
async def add_trade(trade: TradeCreate):
    db = SessionLocal()
    try:
        db_trade = Trade(**trade.model_dump())
        db.add(db_trade)
        db.commit()
        db.refresh(db_trade)
        if trade.price > 100:  # Example threshold
            send_notification.delay(trade.ticker, trade.price, 100)
        return db_trade
    finally:
        db.close()

@app.get("/trades")
async def get_trades(ticker: str = None, start_date: str = None, end_date: str = None):
    db = SessionLocal()
    try:
        query = db.query(Trade)
        if ticker:
            query = query.filter(Trade.ticker == ticker)
        if start_date:
            query = query.filter(Trade.timestamp >= datetime.strptime(start_date, "%Y-%m-%d"))
        if end_date:
            query = query.filter(Trade.timestamp <= datetime.strptime(end_date, "%Y-%m-%d"))
        return query.all()
    finally:
        db.close()