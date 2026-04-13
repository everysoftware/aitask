from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from aitask.commands import BOT_COMMANDS_STR, HELP_STR
from aitask.users.dependencies import UserServiceDep
from aitask.users.keyboards import MAIN_MENU_KB
from aitask.users.schemas import UserCreate

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext, users: UserServiceDep) -> None:
    assert message.from_user is not None
    user = await users.get_by_telegram_id(message.from_user.id)
    if not user:
        data = UserCreate(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        user = await users.register(state, data)
    await message.answer(
        f'{user.display_name}, добро пожаловать в первый таск-трекер с *ИИ* в *Telegram*! 👋\n\nОтправь мне голосовое сообщение: "Добавь задачу купить молоко" и я запишу ее в список. Для просмотра задач скажи: "Покажи задачи" 🎙️\n\nДля навигации используй меню ниже или команды. Узнай больше о боте в разделе "Помощь" ☺️',
        reply_markup=MAIN_MENU_KB,
    )


@router.message(Command("commands"))
async def get_commands(message: types.Message) -> None:
    await message.answer("**Команды**:\n\n" + BOT_COMMANDS_STR)


@router.message(Command("help"))
@router.message(F.text == "Помощь 🧭")
async def get_help(message: types.Message) -> None:
    await message.answer(HELP_STR)
