import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import yapi
import kb

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6636532520:AAGQKEOSpqJjWdikdzCR8qOHwp2WjLx3N44"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

mnc_operator = {'mts': '1', 'megafon': '2', 't2': '25', 'beeline': '99'}

class SetData(StatesGroup):
    ch_operator = State()
    ch_laccid = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Вступительное сообещние по нажатию /start"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
                text= "🪙 БС",
                callback_data= 'bs_info',),
                InlineKeyboardButton(
                text= "📱 Телефон",
                callback_data= 'phone_info'),
    )
    await message.answer("Выберите объект взаимодействия:", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'bs_info')
async def send_bs_info(callback: types.CallbackQuery, state: FSMContext):
    """Выбор оператора и кода mnc"""
    await callback.message.answer('Выбери оператора:', reply_markup=kb.get_keyboard())
    await state.set_state(SetData.ch_operator)


@dp.callback_query(F.data.startswith('operator_'))
async def set_mnc_operator(callback: types.CallbackQuery, state: FSMContext):
    """Сохраняет в памяти MNC оператора"""

    action = callback.data.split('_')[1]

    if action == 'mts':
        await state.update_data(mnc=mnc_operator.get('mts'))
    elif action == 'megafon':
        await state.update_data(mnc=mnc_operator.get('megafon'))
    elif action == 't2':
        await state.update_data(mnc=mnc_operator.get('t2'))
    elif action == 'beeline':
        await state.update_data(mnc=mnc_operator.get('beeline'))
    await callback.message.answer('Введите LAC CID базовой станции через пробел \nДля ввода списком, используйте новую строку для каждой БС')
    
    await state.set_state(SetData.ch_laccid)

@dp.message(SetData.ch_laccid, F.text.regexp(r"^\d{1,9} \d+$"))
async def api_locator(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    bs = message.text.split(" ")
    lac = bs[0]
    cid = bs[1]
    mnc = user_data['mnc']
    print(yapi.push_api(lac=lac, cid=cid, mnc=mnc))
    await message.answer(yapi.push_api(lac=lac, cid=cid, mnc=mnc))


async def main():
    """База"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
