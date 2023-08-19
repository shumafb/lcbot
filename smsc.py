from smsc_api import *

smsc = SMSC()

def get_balance():
    return smsc.get_balance()

def send_ping(phone):
    ping = smsc.send_sms(phone, "", format=6)
    return ping

def send_hlr(phone):
    hlr = smsc.send_sms(phone, "", format=3)
    return hlr

def update_status(id, phone):
    return smsc.get_status(id=id), phone=phone)
