from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
            InlineKeyboardButton(text='Да', callback_data='task_save_confirmed'),
            InlineKeyboardButton(text='Нет', callback_data='task_save_declined')
    ]
    keyboard.add(*buttons)

    return keyboard
