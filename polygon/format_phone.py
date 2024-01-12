def format_phone(phone):
    digits = ''.join(filter(str.isdigit, phone))
    return digits


phone = '7 (994) 494 27-92'

x = format_phone(phone=phone)

print(x)