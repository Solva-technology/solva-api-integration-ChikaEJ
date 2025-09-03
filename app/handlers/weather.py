import os
from http import HTTPStatus

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dotenv import load_dotenv
import aiohttp

from state import MySG

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = os.getenv('OPENWEATHER_BASE_URL')


def format_weather(data: dict) -> str:
    city = data["name"]
    description = data["weather"][0]["description"].capitalize()
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    return (
        f"🌤 Погода в городе *{city}*\n\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"💧 Влажность: {humidity}%\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f"☁️ Состояние: {description}"
    )

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
                text_reply = format_weather(weather)
                return text_reply
            return 'Какая бы не была, погода ты всегда можешь купить пиво, поставить отличный фильм и насладится приятным обществом! '


async def process_city(message: Message, widget, manager: DialogManager):
    city = message.text.strip()
    weather = await get_weather_of_city(city)
    await message.answer(weather)
    await manager.start(MySG.menu, mode=StartMode.RESET_STACK)
