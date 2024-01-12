from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ph_menu(phone):
    '''Клавиатура для взаимодействия с номером телефона'''
    phone_menu_buttons = [
        [
        InlineKeyboardButton(text='🟠📧 SMSC Ping', callback_data='smsc_ping'),
        ],
        [
        InlineKeyboardButton(text='⛔📧 ШЛЮЗ Ping', callback_data='smsc_modemping'),
        ],
        [
        InlineKeyboardButton(text='🟢 WhatsApp', url=f'https://wa.me/+7{phone}'),
        InlineKeyboardButton(text='🔵 Telegram', url=f'https://t.me/+7{phone}'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=phone_menu_buttons)
    return keyboard


def update_ping_status():
    '''Кнопка для взаимодействия с ping-запросом'''
    update_button = [
        [
        InlineKeyboardButton(text='🔄 Обновить', callback_data='update_ping_sms_status')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=update_button)
    return keyboard

def update_modem_ping_status():
    '''Кнопка для взаимодействия с ping-запросом'''
    update_button = [
        [
        InlineKeyboardButton(text='🔄 Обновить', callback_data='update_modem_ping_sms_status')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=update_button)
    return keyboard

def imei_keyboard(imei_device, imei):
    imei_kb = [
        [
            InlineKeyboardButton(text='🟣 IMEI.info', url=f"https://www.imei.info/?imei={imei}"),
            InlineKeyboardButton(text='🔴 Яндекс', url=f"https://ya.ru/search/?text={imei_device}"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=imei_kb)
    return keyboard

def smsc_lk_kb():
    '''Клавиатура для Личного кабинета SMSC'''
    phone_menu_buttons = [
        [
        InlineKeyboardButton(text='📥 История', url=f'https://smsc.ru/sms/'),
        InlineKeyboardButton(text='🌎 На сайт', url=f'https://smsc.ru/user/'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=phone_menu_buttons)
    return keyboard