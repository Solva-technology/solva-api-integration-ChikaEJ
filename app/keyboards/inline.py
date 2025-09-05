from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.state import MySG


async def on_weather(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(MySG.enter_city)


async def on_rps(c: CallbackQuery, b: Button, m: DialogManager):
    await m.start(MySG.rps)
