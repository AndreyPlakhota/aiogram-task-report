from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegistration(StatesGroup):
    adding_user = State()


class AddingTaskStates(StatesGroup):
    adding_task_name = State()
    adding_description = State()
    adding_start_time = State()
    adding_end_time = State()
    save_task = State()
