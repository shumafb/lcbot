import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import yapi, kb as kb, smsc, num, html_parse


logging.basicConfig(level=logging.INFO)

API_TOKEN = "6636532520:AAGQKEOSpqJjWdikdzCR8qOHwp2WjLx3N44"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

mnc_operator = {"mts": "1", "megafon": "2", "t2": "25", "beeline": "99"}


class SetData(StatesGroup):
    ch_operator = State()
    ch_laccid = State()
    ph_get = State()
    ph_menu = State()
    ph_smsc = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Вступительное сообещние по нажатию /start"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📡 БС",
            callback_data="bs_info",
        ),
        InlineKeyboardButton(text="📱 Телефон", callback_data="phone_info"),
    )
    await message.answer(
        "Выберите объект взаимодействия:", reply_markup=builder.as_markup()
    )


# Взаимодействие с БС
@dp.callback_query(F.data == "bs_info")
async def send_bs_info(callback: types.CallbackQuery, state: FSMContext):
    """Выбор оператора и кода mnc"""
    await callback.message.answer("Выбери оператора:", reply_markup=kb.get_keyboard())
    await state.set_state(SetData.ch_operator)


@dp.callback_query(F.data.startswith("operator_"))
async def set_mnc_operator(callback: types.CallbackQuery, state: FSMContext):
    """Сохраняет в памяти MNC оператора"""

    action = callback.data.split("_")[1]

    if action == "mts":
        await state.update_data(mnc=mnc_operator.get("mts"))
    elif action == "megafon":
        await state.update_data(mnc=mnc_operator.get("megafon"))
    elif action == "t2":
        await state.update_data(mnc=mnc_operator.get("t2"))
    elif action == "beeline":
        await state.update_data(mnc=mnc_operator.get("beeline"))
    await callback.message.answer(
        "Введите LAC CID базовой станции через пробел \nДля ввода списком, используйте новую строку для каждой БС"
    )

    await state.set_state(SetData.ch_laccid)


@dp.message(SetData.ch_laccid, F.text.regexp(r"^\d{1,9} \d+$"))
async def api_locator(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    bsinfo = message.text.split(" ")
    lac = bsinfo[0]
    cid = bsinfo[1]
    mnc = user_data["mnc"]
    bsinfo = yapi.push_api(lac=lac, cid=cid, mnc=mnc)
    html_parse.constructor(bslist=bsinfo)
    # with open('test2.html', 'r', encoding='utf-8') as file:
    #     print(file.read())
    document = FSInputFile('test2.html', filename='map.html')
    await bot.send_document(chat_id=message.chat.id, document=document)

# Взаимодействие с номером телефона
@dp.callback_query(F.data == "phone_info")
async def get_phone(callback: types.CallbackQuery, state: FSMContext):
    """Ввод номера телефона для дальнейшего взаимодействия"""
    await callback.message.answer(
        "Введите номер (10 цифр) для дальнейшего взаимодействия:"
    )
    await state.set_state(SetData.ph_get)


@dp.message(SetData.ph_get, F.text.regexp(r"^(\+7|7|8|)?\d{10}$"))
async def menu_phone(message: types.Message, state: FSMContext):
    """Меню взаимодействия с аб.номером"""
    await state.update_data(phone=message.text)
    ph = await state.get_data()
    phone = ph["phone"][-10:]
    info = num.check_phone(phone)
    
    await message.answer(
        f"Номер: {phone} \nОператор: {info['operator']}\nРегион: {info['region']}\nВыберите взаимодействие с одним из сервисов:  ",
        reply_markup=kb.ph_menu(phone=phone))
    await state.set_state(SetData.ph_menu)


@dp.callback_query(F.data == "phmenu_smsc")
async def smsc_phone(callback: types.CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph["phone"][-10:]
    await callback.message.answer(
        f"Номер: {phone} \n Баланс: {smsc.get_balance()} \n Выберите действие:",
        reply_markup=kb.smsc_menu(),
    )
    await state.set_state(SetData.ph_smsc)


@dp.callback_query(F.data.startswith("smsc_"))
async def smsc_action(callback: types.CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph["phone"][-10:]

    action = callback.data.split("_")[1]

    if action == "ping":
        ping = smsc.send_ping(phone=phone)
        await state.update_data(ping=ping)
        await callback.message.answer(smsc.pretty_update_ping(update_ping(ping, phone)), reply_markup=kb.update_ping)
    elif action == "hlr":
        await callback.message.answer(smsc.send_hlr(phone=phone))


@dp.callback_query(F.data == 'update_ping')
async def update_ping(callback: types.CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph['phone'][-10:]
    ping = ph['ping']

    await Bot.edit_message_text(smsc.pretty_update_ping(update_ping(ping, phone)), callback.message.chat.id, callback.message.message_id)


async def main():
    """База"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
