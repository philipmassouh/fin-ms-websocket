import typing as tp
import asyncio
import websockets
import json
import random
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
ROOT = "localhost"
PORT = "8765"

async def market_data(websocket: tp.Any) -> None:
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

    try:
        while True:
            data = dict(
                ticker=random.choice(tickers),
                price=round(random.uniform(50, 500), 2),
                volume=random.randint(1000, 100000),
                timestamp=datetime.now().isoformat()
            )

            await websocket.send(json.dumps(data))
            # https://github.com/python-websockets/websockets/issues/865
            await asyncio.sleep(0.00)

    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"Client disconnected: {e}")
    except Exception as e:
        logger.error(f"Server error: {e}")

async def main():
    server = await websockets.serve(market_data, ROOT, 8765)
    logger.info(f"Server started on ws://{ROOT}:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
