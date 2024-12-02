import asyncio
import json

import websockets


async def ingest_data():
    uri = "ws://localhost:8765/somepath"  # Include the path in the URI
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()  # Receive message from server
                data = json.loads(message)  # Parse the incoming message as JSON

                if data:
                    print(
                        f"Received data: Ticker={data.get('ticker')}, Price={data.get('price')}, Volume={data.get('volume')}, Timestamp={data.get('timestamp')}"
                    )
                else:
                    print("Received duplicate or missing data (skipped).")

            except Exception as e:
                print(f"Error receiving data: {e}")
                break


# Run the ingestion
asyncio.run(ingest_data())
