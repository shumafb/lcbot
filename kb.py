from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# def get_keyboard():
#     operator_buttons = [
#         [
#             InlineKeyboardButton(text = '🔴 МТС', callback_data='operator_mts'),
#             InlineKeyboardButton(text = '🟢 Мегафон', callback_data='operator_megafon'),
#             InlineKeyboardButton(text = '⚫️ Теле2', callback_data='operator_t2'),
#             InlineKeyboardButton(text = '🟡 Билайн', callback_data='operator_beeline'),
#         ]
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=operator_buttons)
#     return keyboard

def ph_menu(phone):
    '''Клавиатура для взаимодействия с номером телефона'''
    phone_menu_buttons = [
        [
        InlineKeyboardButton(text='🔵📧 SMSC Ping', callback_data='smsc_ping'),
        InlineKeyboardButton(text='🔵📧 SMSC Ping ⏰', callback_data='smsc_ping_timer'),
        ],
        [
        InlineKeyboardButton(text='🔵💌 SMSC HLR', callback_data="smsc_hlr"),
        ],
        [
        InlineKeyboardButton(text='🔴📧 ШЛЮЗ Ping', callback_data='smsc_modem_ping'),
        InlineKeyboardButton(text='🔴📧 ШЛЮЗ Ping ⏰', callback_data='smsc_modem_ping_timer'),
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

def update_hlr_status():
    '''Кнопка для взаимодействия с ping-запросом'''
    update_button = [
        [
        InlineKeyboardButton(text='🔄 Обновить', callback_data='update_hlr_sms_status')
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

def lk_smsc_keyboard():
    smsc_keyboard = [
        [
        InlineKeyboardButton(text='📧 SMSC Ping', callback_data='lk_smsc_ping'),
        InlineKeyboardButton(text='💌 SMSC Ping ⏰', callback_data="lk_smsc_ping_timer"),
        ],
        [
        InlineKeyboardButton(text='📧 ШЛЮЗ Ping', callback_data='lk_smsс_modem_ping'),
        InlineKeyboardButton(text='📧 ШЛЮЗ Ping ⏰', callback_data='lk_smsс_modem_ping_timer'),
        ],
        [
        InlineKeyboardButton(text='🟣 SMSC История', url=f"https://smsc.ru/sms/"),
        InlineKeyboardButton(text='🔴 ШЛЮЗ История', callback_data='lk_smsc_modem_history'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=smsc_keyboard)
    return keyboard
