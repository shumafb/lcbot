from smsc_api import *

smsc = SMSC()


def get_balance():
    return smsc.get_balance()

def update_status(id, phone):
    return smsc.get_status(id=id, phone=f"7{phone},", all=1)


# ==================== PING ====================


def send_ping(phone):
    ping = smsc.send_sms(f"7{phone}", "", format=6)
    print(ping, 'send_ping')
    id = ping[0]
    return int(id)

# def update_ping(id, phone):
#     info = update_status(id=id, phone=phone)
#     print(info, 'update_ping')
#     return f"Ping SMS отправлен на номер {info[4]} \nСтоимость {info[5]} руб\nСтатус: {info[7]} \nБаланс: <b>{get_balance()}</b>\nДля обновления статуса нажмите кнопку 'Обновить'"


# ==================== HLR ====================


def send_hlr(phone):
    hlr = smsc.send_sms(f"7{phone}", "", format=3)
    print(hlr, 'send_hlr', type(hlr))
    id = hlr[0]
    return int(id)

# def update_hlr(id, phone):
#     info = update_status(id=id, phone=phone)
#     print(info, 'update_hlr')
#     return f"HLR-запрос к номеру: <b>{info[4]}</b> \nСтоимость {info[5]} руб\nСтатус: {info[7]}\nБаланс: <b>{get_balance()} руб</b>\nДля обновления статуса нажмите кнопку 'Обновить'"


# status = update_ping(2114,"9994492792")
# print(status)




print(get_balance())