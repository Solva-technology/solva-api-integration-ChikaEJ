import logging
import os
from http import HTTPStatus
from typing import Any

import aiohttp
from dotenv import load_dotenv
from services.mongo_client import AsyncMongoDB
from utils.logging import configure_logging

load_dotenv()

configure_logging()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = os.getenv("OPENWEATHER_BASE_URL")

db = AsyncMongoDB(os.getenv("MONGO_URI"), os.getenv("MONGO_DB"))


logging.info("MongoDB connection established", extra={"DB_name": os.getenv("MONGO_DB")})


def format_weather(data: dict) -> dict[str, Any] and str:
    city = data["name"]
    description = data["weather"][0]["description"].capitalize()
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    return (
        {
            "city": city,
            "description": description,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
        },
        f"🌤 Погода в городе *{city}*\n\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"💧 Влажность: {humidity}%\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f"☁️ Состояние: {description}",
    )


async def get_weather_of_city(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    logging.info("sending params to openweather", extra={"city": city})

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == HTTPStatus.OK:
                weather = await response.json()
                data, text = format_weather(weather)
                text_reply = text
                logging.info("received data from openweather", extra={"city": city})

                await db.insert_one(data["city"], data)
                logging.info("add to mongo db", extra={"city": city})

                return text_reply
            logging.warning("Could not get weather data", extra={"city": city})
            return "Какая бы не была, погода ты всегда можешь купить пиво, поставить отличный фильм и насладится приятным обществом! "
