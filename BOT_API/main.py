"""
Исполняющий модуль программы.

Func:

    start: Содержит:
        1. Настройки бота.
        2. Регистрацию роутеров.
        3. Запуск бота в режиме start_polling.
"""
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core.handlers.basic import router, start_bot, stop_bot


async def start():
    """
    Функция инициации и запуска бота.

    Notes:
    
        Входная точка в проект с настройками
        и регистрацией роутеров.
    """
    bot = Bot(token=os.getenv('TOKEN'),
              default=DefaultBotProperties(parse_mode='HTML'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация роутера
    dp.include_router(router)
    
    # Регистрация функций для старта и остановки
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())