from smsc_api import *

smsc = SMSC()


def get_balance():
    return smsc.get_balance()


# ==================== PING ====================


def send_ping(phone):
    ping = smsc.send_sms(f"7{phone}", "", format=6)
    print(ping, 'send_ping')
    return ping


def update_ping(ping, phone):
# def update_ping(id, phone):
    info = update_status(id=ping[0], phone=phone)
    # info = update_status(id=id, phone=phone)
    print(info, 'update_ping')
    return info


def update_status(id, phone):
    return smsc.get_status(id=id, phone=f"7{phone},", all=1)


def pretty_update_ping(info):
    print(info)
    return f"Ping SMS отправлен на номер {info[4]} \nСтоимость {info[5]} руб\nСтатус: {info[7]} \nБаланс: <b>{get_balance()}</b>\nДля обновления статуса нажмите кнопку 'Обновить'"




def send_hlr(phone):
    hlr = smsc.send_sms(f"7{phone}", "", format=3)
    print(hlr)
    info = update_status(id=hlr[0], phone=phone)
    print(info)
    return f"HLR-запрос к номеру: <b>{info[4]}</b> \nСтатус: {info[6]]}\nБаланс: <b>{get_balance()} руб</b>"


# status = update_ping(2114,"9994492792")
# print(pretty_update_ping(status))