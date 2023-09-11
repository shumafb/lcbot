import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

import html_parse
import kb
import num
import smsc
import smsc_api
import yapi

# logging.basicConfig(level=logging.INFO, filename="log/py_bot.log", filemode='w', format="%(asctime)s %(levelname)s %(message)s")
logging.basicConfig(level=logging.INFO)
logging.info('An Info')
logging.error('An Error')


with open("source/info.json", "r", encoding="utf-8") as file:
    file = json.load(file)

with open('source/id_list.txt', 'r', encoding='utf-8') as idlist:
    idlist = idlist.read()
    idlist = idlist.split('\n')
    idlist = list(map(int, idlist))


API_TOKEN = file["telegram_token"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

mnc_operator = {"mts": "1", "megafon": "2", "t2": "25", "beeline": "99"}


class SetData(StatesGroup):
    ph_get = State()
    ph_menu = State()
    ph_smsc = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Вступительное сообещние по нажатию /start"""
    if message.from_user.id not in idlist:
        return message.answer('Нет доступа')
    await message.answer(
        "Введите объект взаимодействия \nили команду /help для вывода информации по боту",  # reply_markup=builder.as_markup()
    )


# ВЗАИМОДЕЙСТВИЕ С БС
# @dp.callback_query(F.data == "bs_info")
# async def send_bs_info(callback: types.CallbackQuery, state: FSMContext):
#     """Выбор оператора и кода mnc"""
#     await callback.message.answer("Выбери оператора:", reply_markup=kb.get_keyboard())
#     await state.set_state(SetData.ch_operator)


# @dp.callback_query(F.data.startswith("operator_"))
# async def set_mnc_operator(callback: types.CallbackQuery, state: FSMContext):
#     """Сохраняет в памяти MNC оператора"""

#     action = callback.data.split("_")[1]

#     if action == "mts":
#         await state.update_data(mnc=mnc_operator.get("mts"))
#     elif action == "megafon":
#         await state.update_data(mnc=mnc_operator.get("megafon"))
#     elif action == "t2":
#         await state.update_data(mnc=mnc_operator.get("t2"))
#     elif action == "beeline":
#         await state.update_data(mnc=mnc_operator.get("beeline"))
#     await callback.message.answer(
#         "Введите LAC CID базовой станции через пробел \nДля ввода списком, используйте новую строку для каждой БС"
#     )

#     await state.set_state(SetData.ch_laccid)


@dp.message(F.text.regexp(r"^(1|2|25|99) (\d{1,8}) (\d+)"))
async def api_locator(message: Message):
    """Принимает mnc lac cid от пользователя и направляет аргументы в Яндекс.Локатор"""
    if message.from_user.id not in idlist:
        return message.answer('Нет доступа')
    bs_info = message.text.split("\n")
    bs_list = []
    yapi_info = []
    pretty_bs_list = []
    count = 0
    for bs in bs_info:
        bs_list.append(bs.split(" "))
    for bs in bs_list:
        mnc = bs[0]
        lac = bs[1]
        cid = bs[2]
        yapi_info.append(yapi.push_api(lac=lac, cid=cid, mnc=mnc))
    for bs in yapi_info:
        pretty_bs_list.append(f"Координаты:\n{count+1}. {lac}-{cid}   |   `{bs['coord'].split('-')[0]} {bs['coord'].split('-')[1]}`")
        count +=1
    html_parse.constructor(bslist=yapi_info)
    document = FSInputFile("test2.html", filename="map.html")
    await message.answer('\n'.join(pretty_bs_list), parse_mode="Markdown")
    await bot.send_document(chat_id=message.chat.id, document=document)


# Взаимодействие с номером телефона
# @dp.callback_query(F.data == "phone_info")
# async def get_phone(callback: types.CallbackQuery, state: FSMContext):
#     """Ввод номера телефона для дальнейшего взаимодействия"""
#     await callback.message.answer(
#         "Введите номер (10 цифр) для дальнейшего взаимодействия:"
#     )
#     await state.set_state(SetData.ph_get)


@dp.message(F.text.regexp(r"^(\+7|7|8|)?\d{10}"))
async def menu_phone(message: Message, state: FSMContext):
    """Меню взаимодействия с аб.номером"""
    if message.from_user.id not in idlist:
        return message.answer('Нет доступа')
    await state.update_data(phone=message.text)
    phone = message.text[-10:]
    info = num.check_phone(phone)

    await message.answer(
        f"Номер: <b>{phone}</b> \nОператор: {info['operator']}\nРегион: {info['region']}\n"
        + f"\nБаланс SMSC: <b>{smsc.get_balance()} руб</b>\nВозможность HLR-запроса: {'🔴' if info['operator'].lower() in 'мегафон' else '🟢'}\n\nВыберите взаимодействие с одним из сервисов:  ",
        reply_markup=kb.ph_menu(phone=phone),
        parse_mode="HTML",
    )
    await state.set_state(SetData.ph_menu)


# @dp.callback_query(F.data == "phmenu_smsc")
# async def smsc_phone(callback: types.CallbackQuery, state: FSMContext):
#     ph = await state.get_data()
#     phone = ph["phone"][-10:]
#     await callback.message.answer(
#         f"Номер: {phone} \n Баланс: {smsc.get_balance()} \n Выберите действие:",
#         reply_markup=kb.smsc_menu(),
#     )
#     await state.set_state(SetData.ph_smsc)


@dp.callback_query(F.data.startswith("smsc_"))
async def smsc_action(callback: CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph["phone"][-10:]

    action = callback.data.split("_")[1]
    print(action, 'action')

    if action == "ping":
        ping = await smsc.send_ping(phone=phone)
        await state.update_data(ping=ping)
        await callback.message.answer(
            smsc.pretty_update_ping(smsc.update_ping(ping=ping, phone=phone)),
            reply_markup=kb.update_status,
            parse_mode="HTML",
        )
    elif action == "hlr":
        await callback.message.answer(smsc.send_hlr(phone=phone), parse_mode="HTML")


@dp.callback_query(F.data == "update_ping")
async def update_ping(callback: CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    print(ph, 'ph_info')
    phone = ph["phone"][-10:]
    print(phone, "phone")
    ping = ph["ping"]
    update_ping_info = await smsc.update_ping(ping, phone)
    print(update_ping_info)
    print(pretty_update_ping(update_ping_info))

    # await Bot.edit_message_text(smsc.pretty_update_ping(update_ping(ping, phone)), callback.message.chat.id, callback.message.message_id)
    await callback.message.answer(
        smsc.pretty_update_ping(update_ping_info),
        reply_markup=kb.update_status,
        parse_mode="HTML")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    if message.from_user.id not in idlist:
        return message.answer('Нет доступа')
    await message.answer("<b>Примеры команд для ввода:</b>\n\n" + \
                         "📱 <b>Поиск по номеру телефона</b>\n" + \
                         "├ 📝 <b>79994492792</b> - ПРИМЕР\n" + \
                         "├ ℹ️ Любой формат (+7..., 8..., 9...)\n" + \
                         "├ 📧 Ping SMS - отправка Ping SMS\n" + \
                         "├ 💌 HLR - отправка HLR-запроса\n" + \
                         "├ 🟢 WhatsApp - переход в WhatsApp\n" + \
                         "└ 🔵 Telegram - переход в Telegram\n\n" + \
                         "📡 <b>Поиск по базовой станции</b>\n" + \
                         "├ 📝 <b>MNC LAC CID</b> - ПРИМЕР\n" + \
                         "├ ℹ️ Возможность работы со <b>списками БС</b>\n"
                         "├ ℹ️ MNC - 1, 2, 25, 99\n" + \
                         "├ ℹ️ LAC - До 8 цифр\n" + \
                         "├ ℹ️ CID - Неограниченное количество цифр\n" + \
                         "└ 🗺️ Отображение координат <b>Базовых Станций</b>",
                         parse_mode="HTML"
                         )


@dp.message(Command('balance'))
async def cmd_balance(message: Message):
    if message.from_user.id not in idlist:
        return message.answer('Нет доступа')
    await message.answer(f"Привет, {smsc_api.SMSC_LOGIN}!\nБаланс SMSC: <b>{smsc.get_balance()} руб</b>", parse_mode="HTML")

@dp.message(Command('id'))
async def cmd_get_id(message:Message):
    # if message.from_user.id not in idlist:
    #     return message.answer('Нет доступа')
    await message.answer(f"Твой Telegram ID: `{message.from_user.id}`", parse_mode="Markdown")

@dp.message(F.text.regexp(r"."))
async def try_again(message: Message):
    if message.from_user.id not in idlist:
        return message.answer('Нет доступа')
    await message.answer('Запрос не распознан\nПопробуйте снова\nили введите команду /help')

# ЗАПУСК БОТА
async def main():
    """База"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
