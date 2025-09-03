from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from handlers.weather import process_city
from state import MySG

from handlers.rps import on_choice


async def on_weather(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(MySG.enter_city)

async def on_rps(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(MySG.rps)


main_dialog = Dialog(
    Window(
Const('Выберите'),
        Row(
            Button(Const('Погода'), id='weather', on_click=on_weather),
            Button(Const('КНБ'), id='rps', on_click=on_rps),
        ),
        state=MySG.menu,
    ),
    Window(
        Const('Введите город'),
        MessageInput(process_city),
        state=MySG.enter_city,
    ),
    Window(
        Const('Выберите одну из них'),
        Row(
            Button(Const('Камень'), id='rock', on_click=on_choice),
                Button(Const('Ножницы'), id='scissors', on_click=on_choice),
                Button(Const('Бумага'), id='paper', on_click=on_choice),
        ),
        state=MySG.rps,
    )
)