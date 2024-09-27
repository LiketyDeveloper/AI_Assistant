from loguru import logger
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from .handlers import router

async def start_telegram_bot():
    """Start the bot"""
    load_dotenv()
    
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode='HTML'))
    
    dp.include_router(router)
    
    ## Delete all pending updates, made before starting the bot
    await bot.delete_webhook(drop_pending_updates=True)  

    logger.success('Bot successfully started')
    
    ## Start the bot 
    await dp.start_polling(bot, skip_updates=True)
    