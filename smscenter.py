import random
import string
import os
import glob


def sent_sms(phone, flag=1):
    file_name = f'/home/user/smscenter/sms/outgoing/{flag}/{phone}-{"".join(random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase) for x in range(6))}.txt'
    with open(file_name, "w", encoding="utf-8") as file:
        x = f"To: 7{phone}\n"
        x += "Report: yes\n"
        x += "Ping: yes\n"
        x += "\ntest"
        file.write(x)


def get_message_id(file_name):
    file_check_id_name = file_name.replace('outgoing', 'sent')
    # file_check_id_name = "/Users/baypso/Documents/codespace/LACator/otstoy/test.txt"
    with open(file_check_id_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in lines:
            if "Message_id" in i:
                return i.split()[1]


def check_status(file_name):
    # Поиск по файлам в папке report
    try:
        directory = '/home/user/smscenter/sms/report/*'
        files = [os.path.abspath(f) for f in glob.glob(directory)]
        for file in files:
            info = {}
            with open(file, 'r', encoding='utf-8') as fl:
                for line in file:
                    if line == "test":
                        continue
                    key, *value = line.split(': ')
                    info[key] = value
                    return info
    except FileNotFoundError:
        pass

    # Поиск по файлам в папке sent
    try:
        directory = '/home/user/smscenter/sms/sent/*'
        files = [os.path.abspath(f) for f in glob.glob(directory)]
        for file in files:
            info = {}
            with open(file, 'r', encoding='utf-8') as fl:
                for line in file:
                    if line == "SMS STATUS REPORT":
                        continue
                    key, *value = line.split(': ')
                    info[key] = value
                    return info
    except FileNotFoundError:
        pass




directory = '/Users/baypso/Documents/codespace/LACator/otstoy/*'


files = [os.path.abspath(f) for f in glob.glob(directory)]

print(files)