from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from app.handlers.rps import on_choice
from app.handlers.weather import weather_of_city
from app.keyboards.inline import on_rps, on_weather
from app.state import MySG

main_dialog = Dialog(
    Window(
        Const("Выберите"),
        Row(
            Button(Const("Погода"), id="weather", on_click=on_weather),
            Button(Const("КНБ"), id="rps", on_click=on_rps),
        ),
        state=MySG.menu,
    ),
    Window(
        Const("Введите город"),
        MessageInput(weather_of_city),
        state=MySG.enter_city,
    ),
    Window(
        Const("Выберите одну из них"),
        Row(
            Button(Const("Камень"), id="rock", on_click=on_choice),
            Button(Const("Ножницы"), id="scissors", on_click=on_choice),
            Button(Const("Бумага"), id="paper", on_click=on_choice),
        ),
        state=MySG.rps,
    ),
)
