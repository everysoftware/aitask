from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from aitask.config import bot_settings

bot = Bot(
    bot_settings.bot_token,
    default=DefaultBotProperties(parse_mode="Markdown"),
)
