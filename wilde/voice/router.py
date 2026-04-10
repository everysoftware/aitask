import logging
import os

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from wilde.bot import bot
from wilde.lists import router as checklists_router
from wilde.lists.dependencies import TodoListServiceDep
from wilde.tasks import router as tasks_router
from wilde.tasks.dependencies import TaskServiceDep
from wilde.users.dependencies import UserDep
from wilde.voice.dependencies import VoiceServiceDep
from wilde.voice.schemas import VoiceCommand

router = Router()


@router.message(F.content_type == types.ContentType.VOICE)
async def handle_voice_message(  # noqa: PLR0913
    message: types.Message,
    user: UserDep,
    service: VoiceServiceDep,
    state: FSMContext,
    tasks: TaskServiceDep,
    checklists: TodoListServiceDep,
) -> None:
    ogg_path = f"temp/voice_{message.from_user.id}.ogg"
    try:
        try:
            file = await bot.get_file(message.voice.file_id)
            assert file.file_path is not None
            await bot.download_file(file.file_path, ogg_path)
        except Exception as e:
            await message.reply("Произошла ошибка при скачивании голосового сообщения")
            logging.info("Error: %s", e)
            raise
        response = await service.help(user, state, ogg_path)
        match response.cmd:
            case VoiceCommand.create_task:
                await message.answer("Задача успешно создана!")
                await tasks_router.get(message, state, tasks, checklists)
            case VoiceCommand.show_tasks:
                await checklists_router.get(message, state, tasks, checklists)
            case VoiceCommand.unknown:
                await message.answer(
                    f"Я распознал ваш запрос: '{response.speech_text}', но не понял, что с ним делать."
                )

    finally:
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
