import asyncio
from smsc_api import *

smsc = SMSC()


def get_balance():
    return smsc.get_balance()


# ==================== PING ====================


def send_ping(phone):
    ping = smsc.send_sms(f"7{phone}", "", format=6)
    return ping


def update_ping(ping, phone):
    info = update_status(id=ping[0], phone=phone)
    return info


def pretty_update_ping(info):
    print(info)
    return f"Ping SMS отправлен на номер {info[4]} \nСтоимость {info[5]} \nСтатус: {info[7]} \nДля обновления статуса нажмите кнопку 'Обновить'"


def send_hlr(phone):
    hlr = smsc.send_sms(f"7{phone}", "", format=3)
    print(hlr)
    info = update_status(id=hlr[0], phone=phone)
    return f"HLR-запрос отправлен на номер: {info[12]} \nСтоимость {info[13]}\n Статус: {info[14]}"


def update_status(id, phone):
    return smsc.get_status(id=id, phone=f"7{phone},", all=1)

