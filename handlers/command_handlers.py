import datetime
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states.states import UserRegistration, AddingTaskStates
from database.db_models import Task
from sqlalchemy import select


async def cmd_start(message: types.Message):
    """
    Отправляет приветсвие
    """
    await message.reply(f'Здравствуйте, {message.from_user.full_name}')


async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Позволяет пользователю отменить текущее состояние
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    # Отменяет состояние пользователя и сообщает об ему об этом
    await state.finish()
    await message.reply('Действие отменено.', reply=False)


async def cmd_add_user(message: types.Message):
    """
    Запускает процесс регистрации пользователя
    """
    await UserRegistration.adding_user.set()
    await message.reply('Введите адрес электронной почты', reply=False)


async def cmd_add_task(message: types.Message):
    """
    Запускает процесс добавления задачи в базу данных
    """
    await AddingTaskStates.adding_task_name.set()
    await message.reply('Введите название задачи (до 30 символов)', reply=False)


async def cmd_show_today_tasks(message: types.Message):
    """
    Отправляет список, добавленных за текущий день задач
    """
    db_session = message.bot.get('db')
    get_tasks_list = select(Task).where(Task.user_id == message.from_user.id, Task.date == datetime.date.today())
    async with db_session() as session:
        tasks_list = await session.execute(get_tasks_list)
        
        result_text = [
            md.text(
                md.text(f'Задача: {md.bold(task.task_name)} ID: {md.bold(task.id)}'),
                md.text(f'Описание: {md.bold(task.description)}'),
                md.text(f'Время начала: {md.bold(task.start_time)}'),
                md.text(f'Время окончания: {md.bold(task.end_time)}'),
                sep='\n'
            ) for task in tasks_list.scalars()
        ]

        await message.bot.send_message(message.from_user.id, '\n\n'.join(result_text), parse_mode=ParseMode.MARKDOWN)


async def delete_task(message: types.Message):
    """
    Позволяет удалить задачу по её id
    """
    await AddingTaskStates.delete_task.set()
    await message.reply('Введите id задачи, которую хотите удалить')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_add_user, commands='adduser')
    dp.register_message_handler(cmd_add_task, commands='addtask')
    dp.register_message_handler(cmd_show_today_tasks, commands='todaytasks')
    dp.register_message_handler(delete_task, commands='deletetask')
