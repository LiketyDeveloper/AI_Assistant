import asyncio
from loguru import logger

from bot import start_telegram_bot

if __name__ == "__main__":
    asyncio.run(start_telegram_bot())
    