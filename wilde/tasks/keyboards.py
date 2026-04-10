from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from wilde.tasks.constants import TASK_STATUSES, TEST_STATUSES


def get_status_kb(statuses: dict[Any, dict[str, Any]], *, cb_prefix: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for status in statuses.values():
        builder.row(
            InlineKeyboardButton(
                text=f"{status["text"]} {status["emoji"]}",
                callback_data=f"{cb_prefix}:{status["name"]}",
            )
        )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


EDIT_TASK_STATUS_KB = get_status_kb(TASK_STATUSES, cb_prefix="set_status")
EDIT_TEST_STATUS_KB = get_status_kb(TEST_STATUSES, cb_prefix="set_test_status")

SHOW_TASK_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить статус 🟢", callback_data="edit_status"),
        ],
        [
            InlineKeyboardButton(text="Изменить описание 💬", callback_data="comment"),
        ],
        [
            InlineKeyboardButton(text="Изменить вложения 🔗", callback_data="report"),
        ],
        [
            InlineKeyboardButton(text="ИИ-анализ ✨", callback_data="complete"),
            InlineKeyboardButton(text="Удалить ❌", callback_data="delete"),
        ],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="to_todo_list")],
    ]
)
