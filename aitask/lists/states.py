from aiogram.fsm.state import State, StatesGroup


class TodoListGroup(StatesGroup):
    get_many = State()
    get = State()
    select_list = State()
    enter_name = State()
    enter_description = State()
    enter_stack = State()
