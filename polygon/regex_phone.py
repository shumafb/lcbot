import re
pattern = re.compile(r'^\+\d{1,9}\s?(\(\d{1,}\)|\d{1,})[-.\s]?\d{1,}[-.\s]?\d{1,}[-.\s]?\d{1,}$')

phone = '+7 456-45'

if pattern.match(phone):
    print('Верно')
else:
    print('Неверно')