from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Message, CallbackQuery
from fast_depends import inject as fast_inject

from aiogram.dispatcher.event.handler import HandlerObject


class DIMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        handler_obj: HandlerObject = data["handler"]

        injected = fast_inject(handler_obj.callback)

        kwargs = dict(data)

        if isinstance(event, Message):
            kwargs["message"] = event
        elif isinstance(event, CallbackQuery):
            kwargs["call"] = event

        kwargs["event"] = event

        return await injected(**kwargs)


def setup_di(dp: Dispatcher) -> None:
    dp.message.middleware(DIMiddleware())
    dp.callback_query.middleware(DIMiddleware())
