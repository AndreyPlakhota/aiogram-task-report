from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """
    Состояния для процесса регистрации пользователя
    """
    adding_user = State()


class AddingTaskStates(StatesGroup):
    """
    Состояния для действий с задачами
    """
    adding_task_name = State()
    adding_description = State()
    adding_start_time = State()
    adding_end_time = State()
    save_task = State()
    delete_task = State()
