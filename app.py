import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import Config, load_config
from database.database import Base
from handlers.command_handlers import register_commands
from handlers.message_handlers import register_message_handlers
from handlers.callback_handlers import register_callback_handlers


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Приветствие'),
        BotCommand(command='adduser', description='Добавление пользователя в базу данных'),
        BotCommand(command='addtask', description='Добавление задачи в базу данных'),
        BotCommand(command='todaytasks', description='Отправляет список, добавленных за текущий день задач'),
        BotCommand(command='deletetask', description='Удаление задачи'),
        BotCommand(command='cancel', description='Сброс состояния пользователя')
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )

    config: Config = load_config()
    engine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}',
        future=True,
        echo=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    storage = MemoryStorage()
    bot = Bot(config.bot.token, parse_mode='HTML')
    bot['db'] = async_sessionmaker
    dp = Dispatcher(bot, storage=storage)

    register_commands(dp)
    register_message_handlers(dp)
    register_callback_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Бот остановлен!')
