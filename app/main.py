import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram_dialog import DialogManager, setup_dialogs, StartMode
from dotenv import load_dotenv

from app.keyboards.main_menu import main_dialog
from app.middlewares.rate_limit import RateLimitMiddleware
from app.services.sessions import clear_sessions, WINDOW
from app.state import MySG

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(main_dialog)
setup_dialogs(dp)


@dp.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.menu, mode=StartMode.RESET_STACK)


async def clear_sessions_task():
    while True:
        await asyncio.sleep(WINDOW)
        clear_sessions()
        print("💾 sessions.json очищен")


async def main():
    dp.update.middleware(RateLimitMiddleware())
    asyncio.create_task(clear_sessions_task())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
