import random

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from state import MySG


def play_rps(your_choice: str) -> str:
    rps_dict = {
        'rock': 'Камень',
        'scissors': 'Ножницы',
        'paper': 'Бумага'
    }
    rps = list(rps_dict.values())

    your_choice_ru = rps_dict[your_choice]

    comp_choice = random.choice(rps)

    if your_choice_ru == comp_choice:
        result = "Ничья 🤝"
    elif (your_choice_ru == "Камень" and comp_choice == "Ножницы") or \
         (your_choice_ru == "Ножницы" and comp_choice == "Бумага") or \
         (your_choice_ru == "Бумага" and comp_choice == "Камень"):
        result = "Вы выиграли 🎉"
    else:
        result = "Вы проиграли 😢"

    return f"Ваш выбор: {your_choice_ru}\nКомпьютер выбрал: {comp_choice}\n➡ {result}"


async def on_choice(callback: CallbackQuery, button: Button, manager: DialogManager):
    choice = button.widget_id
    await callback.answer(play_rps(choice))
    await manager.start(MySG.menu, mode=StartMode.RESET_STACK)