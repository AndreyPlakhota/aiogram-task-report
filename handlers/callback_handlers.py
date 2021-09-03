import datetime

from states.states import AddingTaskStates
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database.db_models import Task
from sqlalchemy.dialects.postgresql import insert


async def save_task(call: types.CallbackQuery, state: FSMContext):
    """
    Позволяет пользователю подтвердить или отменить сохрание задачи в базу данных
    """
    db_session = call.bot.get('db')
    async with state.proxy() as data:
        data['date'] = datetime.date.today()
    if call.data == 'task_save_confirmed':
        add_task = insert(Task).values(
            task_name=data['task_name'],
            description=data['task_description'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            date=data['date'],
            user_id=call.from_user.id
        )
        async with db_session() as session:
            await session.execute(add_task)
            await session.commit()
        await call.message.reply('Задача сохранена', reply=False)
        await state.finish()

    elif call.data == 'task_save_declined':
        await state.finish()
        await call.bot.send_message(call.message.chat.id, 'Сохранение отменено')


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        save_task,
        lambda call: True,
        state=AddingTaskStates.save_task
    )
