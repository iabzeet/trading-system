from api.main import SessionLocal, Trade
from celery import Celery
from datetime import datetime, timedelta, UTC
from collections import defaultdict

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def calculate_avg_price():
    db = SessionLocal()
    try:
        end_time = datetime.now(UTC)
        start_time = end_time - timedelta(minutes=5)
        trades = db.query(Trade).filter(Trade.timestamp >= start_time).all()
        ticker_prices = defaultdict(list)
        for trade in trades:
            ticker_prices[trade.ticker].append(trade.price)
        for ticker, prices in ticker_prices.items():
            avg_price = sum(prices) / len(prices)
            print(f"Average price for {ticker}: {avg_price}")
            # Optionally store in new table
    finally:
        db.close()