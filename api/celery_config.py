from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")
@app.task
def send_notification(ticker: str, price: float, threshold: float):
    print(f"Notification: {ticker} price {price} crossed threshold {threshold}")

