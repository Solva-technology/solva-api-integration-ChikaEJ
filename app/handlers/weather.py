import os
from http import HTTPStatus

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dotenv import load_dotenv
from services.mongo_client import AsyncMongoDB
import aiohttp

from state import MySG

from utils.utilites import format_weather

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = os.getenv('OPENWEATHER_BASE_URL')

db = AsyncMongoDB(os.getenv('MONGO_URI'), os.getenv('MONGO_DB'))

async def get_weather_of_city(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == HTTPStatus.OK:
                weather = await response.json()
                data, text = format_weather(weather)
                text_reply = text

                await db.insert_one(data['city'], data)

                return text_reply
            return 'Какая бы не была, погода ты всегда можешь купить пиво, поставить отличный фильм и насладится приятным обществом! '


async def process_city(message: Message, widget, manager: DialogManager):
    city = message.text.strip()
    weather = await get_weather_of_city(city)
    await message.answer(weather)
    await manager.start(MySG.menu, mode=StartMode.RESET_STACK)
