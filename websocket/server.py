import asyncio
import websockets
import json
import random
from datetime import datetime, timezone

async def send_stock_data(websocket, path):
    try:
        while True:
            data = {
                "ticker": random.choice(["AAPL", "GOOGL", "MSFT"]),
                "price": round(random.uniform(100, 200), 2),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(1)
    except Exception as e:
        import traceback
        print("WebSocket server error:", e)
        traceback.print_exc()

async def main():
    async with websockets.serve(send_stock_data, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
