import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.fsm.state import StatesGroup, State

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6636532520:AAGQKEOSpqJjWdikdzCR8qOHwp2WjLx3N44"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

class SetOperator(StatesGroup):
    choose_operator = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Вступительное сообещние по нажатию /start"""
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
                text= "🪙 БС",
                callback_data= 'bs_info',
    ))
    await message.answer("Я бот-помощник. Информацию по командам смотри в /help", reply_markup=builder.as_markup())


@dp.message(Command("help"))
async def help_info(message: types.Message):
    """Предоставляет информацию по команде /help"""
    await message.answer("/bs - получить информацию по БС\n"
                         "/ping - отправить ping SMS\n"
                         "/hlr - отправить hlr-запрос\n"
                         "/kody - проверка номера через Kody.su"
                         )


def get_keyboard():
    operator_buttons = [
        [
            types.InlineKeyboardButton(text = '🔴 МТС', callback_data='operator_mts'),
            types.InlineKeyboardButton(text = '🟢 Мегафон', callback_data='operator_megafon'),
            types.InlineKeyboardButton(text = '⚫️ Теле2', callback_data='operator_t2'),
            types.InlineKeyboardButton(text = '🟡 Билайн', callback_data='operator_beeline'),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=operator_buttons)
    return keyboard


@dp.callback_query(F.data == 'bs_info')
async def send_bs_info(callback: types.CallbackQuery):
    """Выбор оператора и кода mnc"""
    await callback.message.answer('Выбери оператора:', reply_markup=get_keyboard())

@dp.callback_query(F.data.startswith('operator_'))
async def set_mnc_operator(callback: types.CallbackQuery):
    """Сохраняет в памяти MNC оператора"""
    mnc_operator = None

    action = callback.data.split('_')[1]

    if action == 'mts':
        mnc_operator = '1'
    elif action == 'megafon':
        mnc_operator = '2'
    elif action == 't2':
        mnc_operator = '25'
    elif action == 'beeline':
        mnc_operator = '99'
    await callback.message.answer('Введите LAC CID базовой станции через пробел (Для ввода списком, используйте новую строку для каждой БС)')


async def main():
    """База"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
