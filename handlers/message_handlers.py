import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.dialects.postgresql import insert
from database.db_models import User
from states.states import UserRegistration, AddingTaskStates
from keyboards.inline_keyboards import confirm_keyboard
from database.db_models import Task
from sqlalchemy import select


async def user_registration(message: types.Message, state: FSMContext):
    """
    Обрабатывает введённый пользователем e-mail, затем добавляет пользователя в базу данных
    """
    # TODO Добавить валидацию введённого e-mail
    db_session = message.bot.get('db')
    e_mail = message.text
    add_user = insert(User).values(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name,
        e_mail=e_mail
    )
    async with db_session() as session:
        await session.execute(add_user)
        await session.commit()
    await message.reply('Вы зарегистрированы')
    await state.finish()


async def add_task_name(message: types.Message, state: FSMContext):
    """
    Обрабатывает введённое имя задачи
    """
    async with state.proxy() as data:
        data['task_name'] = message.text

    await AddingTaskStates.adding_description.set()
    await message.reply('Введите описание задачи (до 50 символов)')


async def add_task_description(message: types.Message, state: FSMContext):
    """
    Обрабатывает введённое описание задачи
    """
    async with state.proxy() as data:
        data['task_description'] = message.text

    await AddingTaskStates.adding_start_time.set()
    await message.reply('Введите время начала выполнения задачи в формате чч:мм')


async def add_task_start_time(message: types.Message, state: FSMContext):
    """
    Обрабатывает введённое время начала выполнения задачи
    """
    async with state.proxy() as data:
        data['start_time'] = message.text

    await AddingTaskStates.adding_end_time.set()
    await message.reply('Введите время окончания выполнения задачи')


async def add_task_end_time(message: types.Message, state: FSMContext):
    """
    Обрабатывает введённое время окончания выполнения задачи
    Затем отправляет описание задачи для ознакомления и клавиатуру для подтверждения или отмены сохранения
    """
    async with state.proxy() as data:
        data['end_time'] = message.text

    await message.bot.send_message(
        message.from_user.id,
        md.text(
            md.text(f'Задача: {md.bold(data["task_name"])}'),
            md.text(f'Описание: {data["task_description"]}'),
            md.text('Время начала:', data["start_time"]),
            md.text('Время окончания:', data["end_time"]),
            sep='\n'
        ),
        parse_mode=ParseMode.MARKDOWN
    )
    await AddingTaskStates.save_task.set()
    await message.bot.send_message(message.chat.id, text='Сохранить задачу?', reply_markup=confirm_keyboard())


async def delete_task(message: types.Message, state: FSMContext):
    """
    Удаляет задачу по введённому id
    """
    db_session = message.bot.get('db')
    delete_task_query = select(Task).where(Task.id == int(message.text))
    async with db_session() as session:
        await session.execute(delete_task_query)
    await message.reply('Задача удалена', reply=False)
    await state.finish()


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(user_registration, state=UserRegistration.adding_user)
    dp.register_message_handler(add_task_name, state=AddingTaskStates.adding_task_name)
    dp.register_message_handler(add_task_description, state=AddingTaskStates.adding_description)
    dp.register_message_handler(add_task_start_time, state=AddingTaskStates.adding_start_time)
    dp.register_message_handler(add_task_end_time, state=AddingTaskStates.adding_end_time)
    dp.register_message_handler(delete_task, state=AddingTaskStates.delete_task)
