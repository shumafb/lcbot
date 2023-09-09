import asyncio
import json
import logging

from aiogram import Bot, Dispatcher

import handlers

logging.basicConfig(level=logging.INFO)

with open("key/info.json", "r", encoding="utf-8") as file:
    file = json.load(file)

API_TOKEN = file["telegram_token"]


async def main():
    """Пропуск состояний и запуск бота"""
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
