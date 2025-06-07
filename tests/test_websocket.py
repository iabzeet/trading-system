import asyncio
import websockets
import json

async def test_websocket():
    async with websockets.connect("ws://localhost:8765") as websocket:
        data = json.loads(await websocket.recv())
        assert "ticker" in data
        assert "price" in data
        assert "timestamp" in data

def test_websocket_server():
    asyncio.run(test_websocket())
