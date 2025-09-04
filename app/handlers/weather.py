import logging

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dotenv import load_dotenv
from services.weather_client import get_weather_of_city
from state import MySG

load_dotenv()


async def weather_of_city(message: Message, widget, manager: DialogManager):
    city = message.text.strip()
    weather = await get_weather_of_city(city)
    await message.answer(weather)
    logging.info("send message to bot", extra={"city": city})
    await manager.start(MySG.menu, mode=StartMode.RESET_STACK)
