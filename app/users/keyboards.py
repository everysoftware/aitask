from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задачи ✅"),
        ],
        [
            KeyboardButton(text="Управление списками 📝"),
            KeyboardButton(text="Управление пространствами 📦"),
        ],
        [
            KeyboardButton(text="Статистика 📊"),
            KeyboardButton(text="Помощь 🧭"),
        ],
    ],
    resize_keyboard=True,
)
