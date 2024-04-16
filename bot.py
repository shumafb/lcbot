import asyncio
import json
import logging
import os

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
import alg_luhn
import saveru
import smscenter
import pw_preview

logging.basicConfig(
    level=logging.INFO,
    filename="/home/user/bot/lcbot/log/py_bot.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
# logging.basicConfig(level=logging.INFO)
logging.info("An Info")
logging.error("An Error")


with open("/home/user/bot/lcbot/source/info.json", "r", encoding="utf-8") as file:
    file = json.load(file)

with open("/home/user/bot/lcbot/source/id_list.txt", "r", encoding="utf-8") as idlist:
    idlist = idlist.read()
    idlist = idlist.split("\n")
    idlist = list(map(int, idlist))


API_TOKEN = file["telegram_token"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


mnc_operator = {"mts": "1", "megafon": "2", "t2": "20", "beeline": "99"}


class SetData(StatesGroup):
    ph_get = State()
    ph_menu = State()
    ph_smsc = State()
    smsc_menu = State()


# ВЗАИМОДЕЙСТВИЕ С БС


@dp.message(F.text.regexp(r"^(1|2|20|99) (\d{1,8}) (\d+)"))
async def api_locator(message: Message):
    """Принимает mnc lac cid от пользователя и направляет аргументы в Яндекс.Локатор"""
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    bs_info = message.text.split("\n")
    bs_list = []
    yapi_info = []
    pretty_bs_list = []
    lc_list = []
    count = 0
    for bs in bs_info:
        bs_list.append(bs.split(" "))
    for bs in bs_list:
        mnc = bs[0]
        lac = bs[1]
        cid = bs[2]
        lc_list.append(f"{lac}-{cid}")
        yapi_info.append(yapi.push_api(lac=lac, cid=cid, mnc=mnc))
    for bs in yapi_info:
        if bs["coord"] != "00.000000-00.000000":
            pretty_bs_list.append(
                f"Координаты:\n{count+1}. {lc_list[count]}   |   `{bs['coord'].split('-')[0]} {bs['coord'].split('-')[1]}`"
            )
        else:
            pretty_bs_list.append(
                f"Координаты:\n{count+1}. {lc_list[count]}   |   БС не найдена в Яндекс.Локаторе"
            )
        count += 1
    html_parse.constructor(bslist=yapi_info, lclist=lc_list)
    await pw_preview.main()
    photo = FSInputFile("/home/user/bot/lcbot/source/screen.png", filename="sceen.png")
    document = FSInputFile("/home/user/bot/lcbot/test2.html", filename="map.html")
    await message.answer("\n".join(pretty_bs_list), parse_mode="Markdown")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await bot.send_document(chat_id=message.chat.id, document=document)


# Взаимодействие с IMEI телефона


@dp.message(F.text.regexp(r"\b\d{14}\b"))
async def check_imei(message: Message, state: FSMContext):
    """Взаимодействие с IMEI-номером"""
    imei = message.text[:14]
    full_imei = alg_luhn.luhn(imei)
    loop = asyncio.get_event_loop()
    # imei_device = await loop.run_in_executor(None, db.check_imei, imei)
    imei_device = await loop.run_in_executor(None, yapi.check_imei, full_imei)
    if imei_device == None:
        result = "Отсутствует в базе 🔴"
    else:
        result = "\n".join(imei_device)
        device = imei_device[1].split(": ")[1] + " " + imei_device[3].split(": ")[1]
    await message.answer(
        result,
        reply_markup=kb.imei_keyboard(imei=full_imei, imei_device=device),
        parse_mode="Markdown",
    )


@dp.message(F.text.regexp(r"\b\d{15}\b"))
async def no_imei(message: Message):
    await message.answer("Если вы хотели ввести IMEI-номер, введите 14 цифр")


# Взаимодействие с номером телефона


@dp.message(F.text.regexp(r"^(\+7|7|8|)?\d{10}"))
async def menu_phone(message: Message, state: FSMContext):
    """Меню взаимодействия с аб.номером"""
    loop = asyncio.get_event_loop()
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    if (
        len(message.text.split(" ")) > 1
        and message.text.split(" ")[1].lower() == "смсц"
    ):
        phone = message.text.split(" ")[0][-10:]
        sms_id = await loop.run_in_executor(None, smsc.send_ping, phone)
        await asyncio.sleep(60)
        info = await loop.run_in_executor(None, smsc.update_status, sms_id, phone)
        await message.answer(
            f"⏰ТАЙМЕР⏰\nPing-запрос на <b>{info[4]}</b>\nСтатус на момент отправки: {info[7]}\nБаланс: {smsc.get_balance()}",
            parse_mode="HTML",
            disable_notification=True,
        )
    elif (
        len(message.text.split(" ")) > 1
        and message.text.split(" ")[1].lower() == "модем"
    ):
        phone = message.text.split(" ")[0][-10:]
        phone_info = num.check_phone(phone)
        if phone_info["operator"].lower() == "билайн":
            flag = 2
        else:
            flag = 1
        file_name = await loop.run_in_executor(None, smscenter.sent_sms, phone, flag)
        await asyncio.sleep(60)
        message_id = await loop.run_in_executor(
            None, smscenter.get_message_id, file_name
        )
        mod_ping_info = await loop.run_in_executor(
            None,
            smscenter.check_status,
            message_id["message_id"],
            message_id["filename"],
            message_id["GSM"],
        )
        if len(mod_ping_info) < 11 and len(mod_ping_info) > 5:
            await message.answer(
                text=f"⏰ТАЙМЕР⏰\nPing на номер {mod_ping_info['To'][0]}\nОтправлен: {mod_ping_info['Sent'][0]}\nСтатус: 🟡 Передано оператору\n\nMessage_id: {mod_ping_info['Message_id'][0]}\nModem: {mod_ping_info['Modem'][0]}",
                parse_mode="HTML",
            )
        elif len(mod_ping_info) > 11:
            await message.answer(
                text=f"⏰ТАЙМЕР⏰\nPing на номер {mod_ping_info['From'][0]}\nОтправлен: {mod_ping_info['Sent'][0]}\nПринято:{mod_ping_info['Received'][0]}\nСтатус: 🟢 Доставлено\n\nMessage_id: {mod_ping_info['Message_id'][0]}\nModem: {mod_ping_info['Modem'][0]}",
                parse_mode="HTML",
            )

    else:
        await state.update_data(phone=message.text)
        phone = message.text[-10:]
        info = num.check_phone(phone)
        try:
            info_saveru = await loop.run_in_executor(
                None, saveru.check_phone, int(f"7{phone}")
            )
        except FileNotFoundError:
            info_saveru = None

        text = f"Запрос: <b>{phone}</b> \nОператор: {info['operator']}\nРегион: {info['region']}\n\n"
        try:
            text += f"Бывший оператор: {info['old_operator']}\n"
        except KeyError:
            pass
        # text += f"\nБаланс SMSC: <b>{smsc.get_balance()} руб</b>\nВозможность HLR-запроса:"
        # text += f"{'🔴' if info['operator'].lower() in 'мегафон' else '🟢'} \n\n"
        if info_saveru is not None:
            text += f"📕<b>Возможные имена:</b>\n {', '.join(info_saveru['name'])}\n\n"
        await message.answer(
            text,
            reply_markup=kb.ph_menu(phone=phone),
            parse_mode="HTML",
        )
        await state.set_state(SetData.ph_menu)


@dp.callback_query(F.data.startswith("smsc_"))
async def smsc_action(callback: CallbackQuery, state: FSMContext):
    ph = await state.get_data()
    phone = ph["phone"][-10:]

    action = callback.data.split("_")[1]

    if action == "ping":
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, smsc.send_ping, phone)
        await state.update_data(sms_id=result)
        await callback.message.answer(
            f'Ping на  <b>{phone}</b> отправлен\n Для обновления статуса нажмите кнопку "Обновить"',
            reply_markup=kb.update_ping_status(),
            parse_mode="HTML",
        )

    elif action == "hlr":
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, smsc.send_hlr, phone)
        await state.update_data(sms_id=result)
        await callback.message.answer(
            f'HLR на <b>{phone}</b> отправлен\nДля обновления статуса нажмите кнопку "Обновить"',
            reply_markup=kb.update_hlr_status(),
            parse_mode="HTML",
        )

    elif action == "modemping":
        loop = asyncio.get_event_loop()
        phone_info = num.check_phone(phone)
        if (
            phone_info["operator"].lower() == "билайн"
            or phone_info["operator"].lower() == "вымпелком"
        ):
            flag = 2
        else:
            flag = 1
        file_name = await loop.run_in_executor(None, smscenter.sent_sms, phone, flag)
        await state.update_data(file_name=file_name)
        await callback.message.answer(
            text=f'Ping отправлен на: <b>{phone}</b>\nДля обновления статуса нажмите кнопку "Обновить"',
            reply_markup=kb.update_modem_ping_status(),
            parse_mode="HTML",
        )


@dp.callback_query(F.data == "update_ping_sms_status")
async def update_ping_status(callback: CallbackQuery, state: FSMContext):
    set_info = await state.get_data()
    phone = set_info["phone"][-10:]
    sms_id = set_info["sms_id"]
    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, smsc.update_status, sms_id, phone)
    await callback.message.answer(
        f"Ping-запрос к номеру: <b>{info[4]}</b> \nСтоимость {info[5]} руб\nСтатус: {info[7]}\nБаланс: <b>{smsc.get_balance()} руб</b>\nДля обновления статуса нажмите кнопку 'Обновить'",
        reply_markup=kb.update_ping_status(),
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "update_hlr_sms_status")
async def update_hlr_status(callback: CallbackQuery, state: FSMContext):
    set_info = await state.get_data()
    phone = set_info["phone"][-10:]
    sms_id = set_info["sms_id"]
    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, smsc.update_status, sms_id, phone)
    await callback.message.answer(
        text=f"{info[14]}-запрос к номеру: <b>{info[12]}</b> \nСтоимость {info[13]} руб\nСтатус: {info[15]}\nБаланс: <b>{smsc.get_balance()} руб</b>\nДля обновления статуса нажмите кнопку 'Обновить'",
        reply_markup=kb.update_hlr_status(),
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "update_modem_ping_sms_status")
async def update_modem_ping_status(callback: CallbackQuery, state: FSMContext):
    loop = asyncio.get_event_loop()
    state_info = await state.get_data()
    filename = state_info["file_name"]
    message_id = await loop.run_in_executor(None, smscenter.get_message_id, filename)
    mod_ping_info = await loop.run_in_executor(
        None,
        smscenter.check_status,
        message_id["message_id"],
        message_id["filename"],
        message_id["GSM"],
    )
    print(mod_ping_info)
    if len(mod_ping_info) < 11:
        await callback.message.answer(
            text=f"Ping на {mod_ping_info['To'][0]}\nОтправлен: {mod_ping_info['Sent'][0]}\nСтатус: 🟡 Передано оператору\n\nMessage_id: {mod_ping_info['Message_id'][0]}\nModem: {mod_ping_info['Modem'][0]}",
            reply_markup=kb.update_modem_ping_status(),
            parse_mode="HTML",
        )
    elif len(mod_ping_info) > 11:
        await callback.message.answer(
            text=f"Ping на {mod_ping_info['From'][0]}\nОтправлен: {mod_ping_info['Sent'][0]}\nПринят: {mod_ping_info['Received'][0]}\nСтатус: {mod_ping_info['Status']} /statuslist\n\nMessage_id: {mod_ping_info['Message_id'][0]}\nModem: {mod_ping_info['Modem'][0]}",
            reply_markup=kb.update_modem_ping_status(),
            parse_mode="HTML",
        )


@dp.callback_query(F.data == "update_modem_ping_list_status")
async def update_modem_ping_list_status(callback: CallbackQuery):
    print('check!!')
    with open('/home/user/bot/lcbot/source/ping_status_list.txt', 'r') as file:
        file = file.read()
        print(file)
        await bot.answer_callback_query(callback.id, text=file, show_alert=False)


@dp.message(F.text.regexp(r"^([А-Я]|[а-я]){3,}"))
async def search_fio(message: Message):
    """Принимает фамилию (имя, отчество опционально), выгражает информацию из баз данных"""
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    loop = asyncio.get_event_loop()
    fio = message.text
    info_saveru_fio = await loop.run_in_executor(None, saveru.check_fio, fio)
    status = info_saveru_fio["status"]
    if status == 0:
        await message.answer(
            "<b>Запрос</b>: {fio}\n\n <b>Результаты запроса:</b>\n\n Нет данных",
            parse_mode="HTML",
        )
    elif status == 1:
        text = f"Запрос: *{fio}*\n\n*Имена:*\n{info_saveru_fio['result']['name'][0].strip(', ')}\n\n"
        if info_saveru_fio["result"]["phone_number"][0] != "":
            text += (
                f"*Номер телефона:*\n{info_saveru_fio['result']['phone_number'][0]}\n\n"
            )
        if info_saveru_fio["result"]["birthday_list"][0] != "":
            text += f"*Дни рождения:*\n{info_saveru_fio['result']['birthday_list'][0].strip(', ')}\n\n"
        if info_saveru_fio["result"]["address_list"][0] != "":
            text += f"*Адреса:*\n`{info_saveru_fio['result']['address_list'][0].strip(', ')}`\n\n"
        if info_saveru_fio["result"]["email_list"][0] != "":
            text += f"*Email-адреса:*\n{info_saveru_fio['result']['email_list'][0].strip(', ')}\n\n"
        if info_saveru_fio["result"]["car_list"][0] != "":
            text += f"*Автомобили:*\n{info_saveru_fio['result']['car_list'][0].strip(', ')}\n\n"
        if info_saveru_fio["result"]["car_plate_list"][0] != "":
            text += f"*Госномера авто:*\n{info_saveru_fio['result']['car_plate_list'][0].strip(', ')}"

        await message.answer(text)
    elif status == 2:
        for i in range(len(info_saveru_fio["result"]["name"])):
            text = f"*Ответ №{i+1}*\nЗапрос: *{fio}*\n\n"
            text += f"Возможные имена:\n{info_saveru_fio['result']['name'][i].strip(', ')}\n\n"
            if info_saveru_fio["result"]["birthday_list"][i] != "":
                text += f"Возможные дни рождения:\n{info_saveru_fio['result']['birthday_list'][i].strip(', ')}\n\n"
            if info_saveru_fio["result"]["address_list"][i] != "":
                text += f"Возможные адреса:\n`{info_saveru_fio['result']['address_list'][i].strip(', ')}`\n\n"
            if info_saveru_fio["result"]["email_list"][i] != "":
                text += f"Возможные email-адреса:\n{info_saveru_fio['result']['email_list'][i].strip(', ')}\n\n"
            if info_saveru_fio["result"]["car_list"][i] != "":
                text += f"Возможные автомобили:\n{info_saveru_fio['result']['car_list'][i].strip(', ')}\n\n"
            if info_saveru_fio["result"]["car_plate_list"][i] != "":
                text += f"Возможные госномера авто:\n{info_saveru_fio['result']['car_plate_list'][i].strip(', ')}"

            await message.answer(text, parse_mode="Markdown")
    elif status == 3:
        document = FSInputFile("/home/user/bot/lcbot/result.csv", filename="result.csv")
        await message.answer(
            f"Запрос: {fio}\n\nБольшое количество ответов\nОтвет в виде файла:",
        )
        await bot.send_document(chat_id=message.chat.id, document=document)


# Блок необязательной логики


@dp.message(Command("help"))
async def cmd_help(message: Message):
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    await message.answer(
        "<b>Примеры команд для ввода:</b>\n\n"
        + "📱 <b>Поиск по номеру телефона</b>\n"
        + "├ 📝 <b>9998887766</b> - ПРИМЕР\n"
        + "├ ℹ️ Поиск по базам данных (saverudata)\n"
        + "├ ℹ️ Любой формат (+7..., 8..., 9...)\n"
        + "├ 📧 Ping SMS - отправка Ping SMS\n"
        + "├ 💌 HLR - отправка HLR-запроса\n"
        + "├ 🟢 WhatsApp - переход в WhatsApp\n"
        + "└ 🔵 Telegram - переход в Telegram\n\n"
        + "<b>⏰ Работа с таймером</b>\n\n"
        + "├Пример команд для ввода:\n"
        + "├9998887766 смсц - Ping через SMSC\n"
        + "└9998887766 модем - Ping через МОДЕМ\n\n"
        + "👨‍💼 <b>Поиск по ФИО</b>\n"
        + "├ 📝 <b>[ФАМИЛИЯ (обязательно)]</b> [ИМЯ] - ПРИМЕР ЗАПРОСА\n"
        + "└ ℹ️ Поиск по базам данных (saverudata)\n\n"
        + "🆔 Поиск по IMEI:\n"
        + "├ ℹ️ Узнать модель устройства\n"
        + "├ 🟣 Посмотреть IMEI на imei.info\n"
        + "└ 🔴 Посмотреть фото в Яндексе\n\n"
        + "📡 <b>Поиск по базовой станции</b>\n"
        + "├ 📝 <b>MNC LAC CID</b> - ПРИМЕР\n"
        + "├ ℹ️ Работа со <b>списками БС</b>\n"
        + "├ ℹ️ MNC - 1, 2, 20, 99\n"
        + "├ ℹ️ LAC - До 8 цифр\n"
        + "├ ℹ️ CID - Неограниченное количество цифр\n"
        + "└ 🗺️ Отображение координат <b>БС</b>\n\n"
        + "<b>Список команд:</b>\n\n /help - помощь по командам\n/balance - проверить баланс SMSC\n/smsc - инфо по SMSC\n/id - получить свой Telegram ID\n/log - выгрузить логи\n",
        parse_mode="HTML",
    )


@dp.message(Command("balance"))
async def cmd_balance(message: Message):
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    await message.answer(
        f"Привет, {smsc_api.SMSC_LOGIN}!\nБаланс SMSC: <b>{smsc.get_balance()} руб</b>",
        parse_mode="HTML",
    )


@dp.message(Command("smsc"))
async def smsc_lk(message: Message):
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    await message.answer(
        f"Привет, <b>{smsc_api.SMSC_LOGIN}</b>!\nДобро пожаловать в личный кабинет SMSC.\n\nБаланс: <b>{smsc.get_balance()} руб</b>\n\nВыбери команду или введи /help для справки",
        reply_markup=kb.smsc_lk_kb(),
        parse_mode="HTML",
    )


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\nВведи /help для справки\n/id для получения TelegramID.\n"
    )


@dp.message(Command("id"))
async def cmd_get_id(message: Message):
    # if message.from_user.id not in idlist:
    #     return message.answer('Нет доступа')
    await message.answer(
        f"Твой Telegram ID: `{message.from_user.id}`", parse_mode="Markdown"
    )


@dp.message(Command("log"))
async def get_log(message: Message):
    if message.from_user.id != 303595933:
        return message.answer("Нет доступа")
    document = FSInputFile("/home/user/bot/lcbot/log/py_bot.log", filename="py_bot.log")
    await bot.send_document(chat_id=message.chat.id, document=document)


@dp.message(Command("rebootsms"))
async def reboot_smsserver(message: Message):
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    os.system()


@dp.message(F.text.regexp(r"."))
async def try_again(message: Message):
    if message.from_user.id not in idlist:
        return message.answer("Нет доступа")
    await message.answer(
        "Запрос не распознан\nПопробуйте снова\nили введите команду /help"
    )


# ЗАПУСК БОТА
async def main():
    """База"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
