import random, string


def sent_sms(phone, flag):
    print('HELLO')
    with open(f'/home/user/smscenter/sms/outgoing/{flag}/{phone}-{"".join(random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase) for x in range(6))}.txt', 'w', encoding='utf-8') as file:
        x = f"To: 7{phone}\n"
        x += "Report: yes\n"
        x += "\ntest"
        file.write(x)


# sent_sms('9994492792', 1)