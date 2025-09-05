from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.services import sessions


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user_id = None
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id

        if not user_id:
            return await handler(event, data)

        allowed = sessions.add_request(user_id)
        if not allowed:
            if event.message:
                await event.message.answer(
                    "⛔ Слишком много запросов. Попробуйте через 2 минуты."
                )
            elif event.callback_query:
                await event.callback_query.answer(
                    "⛔ Слишком много запросов. Подождите немного.", show_alert=True
                )
            return

        return await handler(event, data)
