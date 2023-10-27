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

# ==================== HLR ====================


def send_hlr(phone):
    hlr = smsc.send_sms(f"7{phone}", "", format=3)
    print(hlr, 'send_hlr', type(hlr))
    id = hlr[0]
    return int(id)
