import re

from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards import kb
from modules import num, smsc

router = Router()

class SetData(StatesGroup):
    laccid = State()
    phone = State()
    # imei = State()
    # imsi = State()

@router.message(Command('start'))
async def cmd_start(message: Message):
    '''Роутер на команду старт'''
    await message.answer('Введите объект взаимодействия')


# ВЗАИМОДЕЙСТВИЕ С НОМЕРОМ ТЕЛЕФОНА
@router.message(F.text.regexp(r"^(\+7|7|8|)?\d{10}$"))
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    phone = await state.get_data()
    phone = phone['phone'][-10:]
    info = num.check_phone(phone=phone)

    await message.answer(
        f"Номер: {phone} \nОператор: {info['operator']}\nРегион: {info['region']}" + \
        "\nВыберите взаимодействие с одним из сервисов:  ",
        reply_markup=kb.phone_menu(phone=phone))
    await state.set_data(SetData.phone)

@router.callback_query(F.data.startswith("smsc_"))
async def smsc_action(callback: CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph["phone"][-10:]

    action = callback.data.split("_")[1]

    if action == "ping":
        ping = smsc.send_ping(phone=phone)
        await state.update_data(ping=ping)
        await callback.message.answer(smsc.pretty_update_ping(update_ping(ping, phone)), reply_markup=kb.update_ping)
    elif action == "hlr":
        await callback.message.answer(smsc.send_hlr(phone=phone))


@router.callback_query(F.data == 'update_ping')
async def update_ping(callback: CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph['phone'][-10:]
    ping = ph['ping']

    await Bot.edit_message_text(smsc.pretty_update_ping(update_ping(ping, phone)), callback.message.chat.id, callback.message.message_id)




# ВЗАИМОДЕЙСТВИЕ С LAC CID

def shell(command):
    """Shell для обработки команд"""
    commandl = command.split("\\n")
    # print(commandl)
    for command in commandl[:-1]:
        if re.search(r"^(\+7|7|8|)?\d{10}$", command):
            print("phone number")
        elif re.search(r"^(1|01|2|02|25|99) (\d{1,8}) (\d+)$", command):
            print("laccid")
        elif re.search(r"\b\d{14}\b", command):
            print("imei")
        elif re.search(r"\b\d{15}\b", command):
            print("imsi")
        else:
            print("error")






