from smsc_api import *

smsc = SMSC()


def get_balance():
    return smsc.get_balance()


# ==================== PING ====================


def send_ping(phone):
    ping = smsc.send_sms(f"7{phone}", "", format=6)
    print(ping)
    return ping


def update_ping(ping, phone):
    info = update_status(id=ping[0], phone=phone)
    print(info)
    return info


def update_status(id, phone):
    return smsc.get_status(id=id, phone=f"7{phone},", all=1)


def pretty_update_ping(info):
    print(info)
    return f"Ping SMS отправлен на номер {info[4]} \nСтоимость {info[5]} \nСтатус: {info[7]} \nБаланс: <b>{get_balance()}</b>\nДля обновления статуса нажмите кнопку 'Обновить'"


def send_hlr(phone):
    hlr = smsc.send_sms(f"7{phone}", "", format=3)
    print(hlr)
    info = update_status(id=hlr[0], phone=phone)
    print(info)
    return f"HLR-запрос к номеру: <b>{info[12]}</b> \nСтатус: {info[15]}\nБаланс: <b>{get_balance()} руб</b>"
