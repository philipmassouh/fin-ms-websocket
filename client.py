import asyncio
import websockets
import json
from server import ROOT, PORT

async def market_data_client():
    uri = f"ws://{ROOT}:{PORT}"

    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(f"Received: {json.loads(message)}")


if __name__ == "__main__":
    asyncio.run(market_data_client())
