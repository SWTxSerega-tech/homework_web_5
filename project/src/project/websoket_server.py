import asyncio
import json
from datetime import datetime

import websockets
from aiofile import async_open
from aiopath import AsyncPath

from main import CurrencyService


LOG_DIR = AsyncPath("logs")
LOG_FILE = LOG_DIR / "exchange.log"


async def write_log(message: str):
    await LOG_DIR.mkdir(parents=True, exist_ok=True)

    async with async_open(LOG_FILE, "a") as afp:
        await afp.write(message + "\n")


async def handle_exchange(command: str):
    parts = command.split()

    days = 1
    currencies = ["EUR", "USD"]

    if len(parts) >= 2:
        try:
            days = int(parts[1])

            if days < 1 or days > 10:
                return {
                    "error": "Maximum 10 days allowed"
                }

        except ValueError:
            currencies = parts[1:]

    if len(parts) >= 3:
        currencies = parts[2:]

    service = CurrencyService(currencies)

    result = await service.get_rates(days)

    return result


async def chat_handler(websocket):
    async for message in websocket:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        await write_log(f"{timestamp} {message}")

        if message.startswith("exchange"):
            result = await handle_exchange(message)

            await websocket.send(
                json.dumps(result, indent=2, ensure_ascii=False)
            )
        else:
            await websocket.send("Unknown command")


async def main():
    async with websockets.serve(chat_handler, "localhost", 8080):
        print("WebSocket server started on ws://localhost:8080")

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
