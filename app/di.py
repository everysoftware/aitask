from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import CallbackQuery, Message, TelegramObject
from fast_depends import inject as fast_inject

if TYPE_CHECKING:
    from aiogram.dispatcher.event.handler import HandlerObject


class DIMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],  # noqa: ARG002
        event: TelegramObject,
        data: dict[str, Any],
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
