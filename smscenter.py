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
        x += "\n "
        file.write(x)
    return file_name[file_name.find("/outgoing/") + 12:]


def get_message_id(file_name):
    file_check_id_name = f"/home/user/smscenter/sms/sent/{file_name}" 
    with open(file_check_id_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in lines:
            if 'Modem' in i:
                gsm_number = i.split()[1]
            if "Message_id" in i:
                return {'message_id': i.split()[1], 'filename': file_name, 'GSM': gsm_number}


def check_status(message_id, filename, gsm_number):
    # Поиск по файлам в папке report
    result = {}
    try:
        directory = "/home/user/smscenter/sms/report/*"
        files = [os.path.abspath(f) for f in glob.glob(directory)]
        for file in files:
            with open(file, "r", encoding="utf-8") as fl:
                lines = fl.readlines()
                info = {}
                for line in lines:
                    line = line.strip("\n")
                    if (
                        line == "test"
                        or line == None
                        or line == "\n"
                        or line == "SMS STATUS REPORT"
                        or line == ""
                    ):
                        continue
                    info[line.split(": ")[0]] = line.split(": ")[1:]
                if info["Message_id"][0] == str(message_id) and info["Modem"][0] == str(gsm_number):
                    result = info
                    print(result)
                    return result
                else:
                    continue
    except FileNotFoundError:
        pass
    if result == {}:
        # Поиск по файлам в папке sent
        try:
            file = f"/home/user/smscenter/sms/sent/{filename}" 
            info = {}
            with open(file, "r", encoding="utf-8") as fl:
                lines = fl.readlines()
                for line in lines:
                    line = line.strip("\n")
                    if (
                        line == " "
                        or line == None
                        or line == "\n"
                        or line == "SMS STATUS REPORT"
                    ):
                        continue
                    key, *value = line.split(": ")
                    info[line.split(": ")[0]] = line.split(": ")[1:]
                print(info, type(info), 'START1111')
                if info["Message_id"][0] == str(message_id) and info["Modem"][0] == str(gsm_number):
                    print(info, type(info), 'STOP1111')
                    result = info
                    return result
        except FileNotFoundError:
            pass
