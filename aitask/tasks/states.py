from aiogram.fsm.state import State, StatesGroup


class TaskGroup(StatesGroup):
    get = State()
    get_many = State()
    enter_name = State()
    enter_status = State()
    enter_comment = State()
    enter_report_url = State()
