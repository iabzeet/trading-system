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