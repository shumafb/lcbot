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
            if "Message_id" in i:
                return {'message_id': i.split()[1], 'filename': file_name}


def check_status(message_id, filename):
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
                if info["Message_id"][0] == str(message_id):
                    result = info
                    return result
                else:
                    continue
    except FileNotFoundError:
        pass
    # if result == {}:
    #     # Поиск по файлам в папке failed
    #     try:
    #         directory = f"/home/user/smscenter/sms/failed/{filename}"
    #         info = {}
    #         with open(file, "r", encoding="utf-8") as fl:
    #             lines = fl.readlines()
    #             for line in lines:
    #                 line = line.strip("\n")
    #                 if (
    #                     line.startswith("To") is True
    #                     or line.startswith("Modem") is True
    #                     or line.startswith("Fail_reason") is True
    #                     or line.startswith("Failed") is True):
    #                     key, *value = line.split(": ")
    #                     info[line.split(": ")[0]] = line.split(": ")[1:]
    #                 else:
    #                     continue
    #                 return result
    #     except FileNotFoundError:
    #         pass
    if result == {}:
        # Поиск по файлам в папке sent
        try:
            directory = "/home/user/smscenter/sms/sent/*"
            files = [os.path.abspath(f) for f in glob.glob(directory)]
            for file in files:
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
                    if info["Message_id"][0] == str(message_id):
                        result = info
                        return result
                    else:
                        continue
        except FileNotFoundError:
            pass
