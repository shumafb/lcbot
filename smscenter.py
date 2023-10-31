import random, string


def sent_sms(phone, flag=1):
    print('HELLO')
    file_name = f'/home/user/smscenter/sms/outgoing/{flag}/{phone}-{"".join(random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase) for x in range(6))}.txt'
    with open(file_name, 'w', encoding='utf-8') as file:
        x = f"To: 7{phone}\n"
        x += "Report: yes\n"
        x += "Ping: yes\n"
        x += "\ntest"
        file.write(x)


def check_status(file_name):
    file_check_name = file_name.replace('outgoing', 'sent')
    with open(file_check_name, 'r', encoding='uft-8') as file:
        file.readlines()