from typing import Any


def format_weather(data: dict) -> dict[str, Any] and str:
    city = data['name']
    description = data['weather'][0]['description'].capitalize()
    temp = round(data['main']['temp'])
    feels_like = round(data['main']['feels_like'])
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    return ({
        'city': city,
        'description': description,
        'temp': temp,
        'feels_like': feels_like,
        'humidity': humidity,
        'wind_speed': wind_speed
    },
        f"🌤 Погода в городе *{city}*\n\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"💧 Влажность: {humidity}%\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f"☁️ Состояние: {description}"
    )
