import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from aitask.cache.config import cache_settings
from aitask.cache.connection import redis_client
from aitask.cache.lifespan import ping_redis
from aitask.commands import BOT_COMMANDS
from aitask.di import setup_di
from aitask.routing import main_router
from aitask.stats.config import stats_settings

from .bot import bot as tg_bot


async def on_startup(bot: Bot) -> None:
    await ping_redis()
    await bot.set_my_commands(BOT_COMMANDS)
    os.makedirs(stats_settings.stats_dir, exist_ok=True)


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    pass


storage = RedisStorage(
    redis=redis_client,
    state_ttl=cache_settings.state_ttl,
    data_ttl=cache_settings.data_ttl,
)
dp = Dispatcher(storage=storage)
setup_di(dp)
dp.include_router(main_router)
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


def main() -> None:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(tg_bot))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
