import asyncio
import websockets
import json
from datetime import datetime, timedelta
from collections import defaultdict

price_history = defaultdict(list)

async def monitor_prices():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            data = json.loads(await websocket.recv())
            ticker = data["ticker"]
            price = data["price"]
            timestamp = datetime.fromisoformat(data["timestamp"])

            # Store price in 1-minute window
            price_history[ticker].append((timestamp, price))
            price_history[ticker] = [(t, p) for t, p in price_history[ticker] if timestamp - t < timedelta(minutes=1)]

            # Calculate price change
            if len(price_history[ticker]) >= 2:
                old_price = price_history[ticker][0][1]
                price_change = ((price - old_price) / old_price) * 100
                if abs(price_change) > 2:
                    print(f"Alert: {ticker} price changed by {price_change:.2f}%: {old_price} -> {price}")

asyncio.run(monitor_prices())