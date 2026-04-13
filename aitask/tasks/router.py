import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from aitask.base.types import UUID
from aitask.base.types import UUID as ID
from aitask.bot import bot
from aitask.lists import router as todo_lists_router
from aitask.lists.dependencies import TodoListServiceDep
from aitask.tasks.constants import TASK_STATUSES
from aitask.tasks.dependencies import TaskServiceDep
from aitask.tasks.keyboards import (
    EDIT_TASK_STATUS_KB,
    EDIT_TEST_STATUS_KB,
    SHOW_TASK_KB,
)
from aitask.tasks.schemas import TaskStatus, TestStatus
from aitask.tasks.states import TaskGroup
from aitask.users.dependencies import UserDep
from aitask.utils import md_to_html, split_msg_html

router = Router()


# CREATE
@router.callback_query(F.data == "add", TaskGroup.get_many)
async def get_name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Назовите задачу. Например, `составить конспект по Римской империи`")
    await state.set_state(TaskGroup.enter_name)
    await call.answer()


@router.message(TaskGroup.enter_name)
async def create(
    message: types.Message,
    state: FSMContext,
    user: UserDep,
    service: TaskServiceDep,
    todo_list_service: TodoListServiceDep,
) -> None:
    user_data = await state.get_data()
    todo_list_id = user_data["todo_list_id"]
    workspace_id = user_data["workspace_id"]
    name = message.text
    await service.create(
        workspace_id=workspace_id,
        todo_list_id=todo_list_id,
        user_id=user.id,
        name=name,
    )
    await message.answer("Задача успешно создана!")

    await todo_lists_router.get(message, state, service, todo_list_service, todo_list_id=todo_list_id)


# GET
@router.callback_query(F.data.startswith("show_task:"), TaskGroup.get_many)
async def get(
    event: types.CallbackQuery | types.Message,
    state: FSMContext,
    service: TaskServiceDep,
    todo_list_service: TodoListServiceDep,
    task_id: ID | None = None,
) -> None:
    user_data = await state.get_data()

    if isinstance(event, types.CallbackQuery):
        message = event.message
        task_id = UUID(event.data.split(":")[1])
    else:
        message = event
        if task_id is None:
            task_id = user_data["task_id"]
    assert task_id is not None

    task = await service.get_one(task_id)
    report_url = task.report_url if task.report_url else "нет"
    desc = task.description if task.description else "нет"

    todo_list_id = user_data["todo_list_id"]
    todo_list = await todo_list_service.get_one(todo_list_id)

    await message.answer(
        f"✅ *{task.name}*\n\n"
        f"Список: {todo_list.name}\n"
        f"Статус: {TASK_STATUSES[task.status]["text"]} {TASK_STATUSES[task.status]["emoji"]}\n"
        f"Описание: {desc}\n"
        f"Вложения: {report_url}\n"
        f"Создано: {task.created_at}\n"
        f"Изменено: {task.updated_at}",
        reply_markup=SHOW_TASK_KB,
    )

    await state.set_state(TaskGroup.get)
    await state.update_data(task_id=str(task_id))
    if isinstance(event, types.CallbackQuery):
        await event.answer()


# EDIT REPORT
@router.callback_query(F.data == "report", TaskGroup.get)
async def enter_url(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введите ссылку на вложения к задаче")
    await state.set_state(TaskGroup.enter_report_url)
    await call.answer()


@router.message(TaskGroup.enter_report_url)
async def edit_report(
    message: types.Message,
    state: FSMContext,
    todo_list_service: TodoListServiceDep,
    service: TaskServiceDep,
) -> None:
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, report_url=message.text)
    await message.answer("Вложения к задаче успешно обновлены!")
    await get(message, state, service, todo_list_service, task_id=task_id)


# EDIT STATUS
@router.callback_query(F.data == "edit_status", TaskGroup.get)
async def enter_status(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Выберите новый статус задачи", reply_markup=EDIT_TASK_STATUS_KB)
    await state.set_state(TaskGroup.enter_status)
    await call.answer()


@router.callback_query(F.data.startswith("set_status:"), TaskGroup.enter_status)
async def edit_status(
    call: types.CallbackQuery,
    state: FSMContext,
    todo_list_service: TodoListServiceDep,
    service: TaskServiceDep,
) -> None:
    new_status = call.data.split(":")[1]
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, status=new_status)
    await call.message.answer("Статус задачи успешно изменен!")
    await get(call.message, state, service, todo_list_service, task_id=task_id)
    await call.answer()


# EDIT TEST STATUS
@router.callback_query(F.data == "edit_test_status", TaskGroup.get)
async def enter_test_status(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Выберите новый статус теста", reply_markup=EDIT_TEST_STATUS_KB)
    await state.set_state(TaskGroup.enter_status)
    await call.answer()


@router.callback_query(F.data.startswith("set_test_status:"), TaskGroup.enter_status)
async def edit_test_status(
    call: types.CallbackQuery,
    state: FSMContext,
    todo_list_service: TodoListServiceDep,
    service: TaskServiceDep,
) -> None:
    test_status = call.data.split(":")[1]
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    if test_status != TestStatus.no_status:
        await service.update(task_id, status=TaskStatus.done, test_status=test_status)
    else:
        await service.update(task_id, test_status=test_status)
    await call.message.answer("Статус теста успешно изменен!")
    await get(call.message, state, service, todo_list_service, task_id=task_id)
    await call.answer()


# EDIT COMMENT
@router.callback_query(F.data == "comment", TaskGroup.get)
async def text(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введите новый комментарий")
    await state.set_state(TaskGroup.enter_comment)
    await call.answer()


@router.message(TaskGroup.enter_comment)
async def edit_comment(
    message: types.Message,
    state: FSMContext,
    todo_list_service: TodoListServiceDep,
    service: TaskServiceDep,
) -> None:
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, description=message.text)
    await message.answer("Комментарий успешно обновлен!")

    await get(message, state, service, todo_list_service, task_id=task_id)


@router.callback_query(F.data == "complete", TaskGroup.get)
async def solve(
    call: types.CallbackQuery,
    state: FSMContext,
    service: TaskServiceDep,
) -> None:
    await call.answer()
    await bot.send_chat_action(call.message.chat.id, "typing")
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    full_text = await service.solve(task_id)
    full_text = md_to_html(full_text)
    logging.info("Full_text: %s", full_text)
    for part in split_msg_html(full_text):
        await call.message.answer(part, parse_mode="HTML")


# EDIT COMMENT
@router.callback_query(F.data == "delete", TaskGroup.get)
async def delete(
    call: types.CallbackQuery,
    state: FSMContext,
    service: TaskServiceDep,
    todo_list_service: TodoListServiceDep,
) -> None:
    await call.answer()
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.delete(task_id)
    await call.message.answer("Задача успешно удалена!")
    await todo_lists_router.get(call.message, state, service, todo_list_service)
