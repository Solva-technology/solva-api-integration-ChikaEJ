from unittest.mock import AsyncMock

import pytest
from aiogram_dialog import StartMode
from aiogram_dialog.test_tools.mock_dialog_manager import MockDialogManager

from app.keyboards.main_menu import main_dialog
from app.state import MySG


@pytest.mark.asyncio
async def test_menu_start():
    dialog_manager = MockDialogManager()

    # Запускаем диалог с состояния меню
    await main_dialog.start(
        chat_id=1,
        user_id=42,
        manager=dialog_manager,
        mode=StartMode.RESET_STACK,
        state=MySG.menu,
    )

    # Проверяем текущее окно
    window = dialog_manager.current_window()
    assert window.text == "Выберите"
    assert len(window.buttons) == 2  # "Погода" и "КНБ"


@pytest.mark.asyncio
async def test_weather_button(monkeypatch):
    dialog_manager = MockDialogManager()

    await main_dialog.start(
        chat_id=1,
        user_id=42,
        manager=dialog_manager,
        mode=StartMode.RESET_STACK,
        state=MySG.menu,
    )

    # Мокаем обработчик on_weather
    called = {}

    async def fake_on_weather(c, b, m):
        called["ok"] = True
        await m.switch_to(MySG.enter_city)

    monkeypatch.setattr("app.keyboards.inline.on_weather", fake_on_weather)

    # Симулируем клик на кнопку "Погода"
    callback = AsyncMock(data="weather", message=AsyncMock())
    button = dialog_manager.current_window().buttons[0]
    await button.on_click(callback, button, dialog_manager)

    assert called["ok"]
    assert dialog_manager.current_state() == MySG.enter_city


@pytest.mark.asyncio
async def test_rps_button(monkeypatch):
    dialog_manager = MockDialogManager()

    await main_dialog.start(
        chat_id=1,
        user_id=42,
        manager=dialog_manager,
        mode=StartMode.RESET_STACK,
        state=MySG.menu,
    )

    called = {}

    async def fake_on_rps(c, b, m):
        called["ok"] = True
        await m.switch_to(MySG.rps)

    monkeypatch.setattr("app.keyboards.inline.on_rps", fake_on_rps)

    # Симулируем клик на кнопку "КНБ"
    callback = AsyncMock(data="rps", message=AsyncMock())
    button = dialog_manager.current_window().buttons[1]
    await button.on_click(callback, button, dialog_manager)

    assert called["ok"]
    assert dialog_manager.current_state() == MySG.rps
