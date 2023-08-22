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

def ph_menu(phone):
    phone_menu_buttons = [
        [
        InlineKeyboardButton(text='☎️ Kody.su', callback_data='phmenu_kody'),
        # InlineKeyboardButton(text='📞 GetContact', callback_data='phmenu_getcontact'),
        InlineKeyboardButton(text='📩 SMSC', callback_data="phmenu_smsc"),
        InlineKeyboardButton(text='🟢 WhatsApp', url=f'https://wa.me/+7{phone}'),
        InlineKeyboardButton(text='🔵 Telegram', url=f'https://t.me/+7{phone}'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=phone_menu_buttons)
    return keyboard


def smsc_menu():
    phone_menu_buttons = [
        [
        InlineKeyboardButton(text='🏳️ Отправить Ping SMS', callback_data='smsc_ping'),
        InlineKeyboardButton(text='📩 Отправить HLR-запрос', callback_data="smsc_hlr"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=phone_menu_buttons)
    return keyboard


def update_ping():
    update_button = [
        InlineKeyboardButton(text='♻️ Обновить', callback_data='update_ping')
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=update_button)
    return keyboard