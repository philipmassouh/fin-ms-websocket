import asyncio
import json
import random
import time

import websockets

tickers = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]


def generate_random_data(ticker):
    price = round(random.uniform(100, 2000), 2)
    volume = random.randint(100, 10000)
    timestamp = int(time.time() * 1000)
    data = {
        "ticker": ticker,
        "price": price,
        "volume": volume,
        "timestamp": timestamp,
    }

    if random.random() < 0.1:
        data["price"] += random.uniform(-1, 1)
        data["volume"] += random.randint(-10, 10)

    if random.random() < 0.2:
        if random.random() < 0.5:
            data["price"] = None
        else:
            data["volume"] = None

    if random.random() < 0.05:
        return None

    return data


async def market_data(websocket, path):
    last_sent_data = {}

    while True:
        try:
            ticker = random.choice(tickers)
            data = generate_random_data(ticker)

            if data is None:
                continue  # Skip sending None data

            message = json.dumps(data)
            await websocket.send(message)
            last_sent_data[ticker] = data

            # Optional: Introduce a small delay between messages to avoid overwhelming the client
            await asyncio.sleep(0.1)  # Reduced delay for high-frequency updates

        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed unexpectedly. Reconnecting...")
            break  # Exit to reconnect loop
        except Exception as e:
            print(f"Error sending message: {e}")
            break  # Exit to reconnect loop


async def start_server():
    """Start the WebSocket server with infinite error handling."""
    while True:
        try:
            print("Starting WebSocket server...")
            server = await websockets.serve(
                market_data, "localhost", 8765, ping_interval=10, ping_timeout=5
            )
            print("Server is running on ws://localhost:8765")

            await server.wait_closed()  # This will ensure that the server runs indefinitely
        except Exception as e:
            print(f"Error occurred while running server: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Retry every 5 seconds if server stops unexpectedly


async def main():
    """Main function to ensure the server keeps running."""
    await start_server()


# Start the server with resilience and minimal downtime
asyncio.run(main())
