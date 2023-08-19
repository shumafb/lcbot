from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def get_keyboard():
    operator_buttons = [
        [
            InlineKeyboardButton(text = '🔴 МТС', callback_data='operator_mts'),
            InlineKeyboardButton(text = '🟢 Мегафон', callback_data='operator_megafon'),
            InlineKeyboardButton(text = '⚫️ Теле2', callback_data='operator_t2'),
            InlineKeyboardButton(text = '🟡 Билайн', callback_data='operator_beeline'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=operator_buttons)
    return keyboard
