# Trading System Assignment
## Setup
- Install Python 3.9+, PostgreSQL, AWS CLI.
- Clone repo: `git clone <repo-url>`
- Install dependencies: `pip install -r requirements.txt`
- Set up PostgreSQL: `createdb trading_system`
- Configure AWS: `aws configure`
## Running
- API: `uvicorn api.main:app --reload`
- WebSocket: `python websocket/server.py & python websocket/client.py`
- Lambda: Deploy via AWS Console or CLI.
## Assumptions
- Mock WebSocket server for real-time data.
- Sample CSV for trading strategy.
## API Setup
- Start PostgreSQL and Redis.
- Run API: `uvicorn api.main:app --reload`
- Test endpoints:
  - POST `/trades`: `curl -X POST http://localhost:8000/trades -d '{"ticker":"AAPL","price":150.0,"quantity":10,"side":"buy"}'`
  - GET `/trades`: `curl http://localhost:8000/trades?ticker=AAPL`
## WebSocket Setup
- Start server: `python websocket/server.py`
- Start client: `python websocket/client.py`
- Alerts printed for >2% price changes.
- Average prices calculated every 5 minutes via Celery.