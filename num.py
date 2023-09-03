import requests

url = "http://num.voxlink.ru/get/?num=+7"


def check_phone(phone):
    response = requests.get(url=url+phone)
    info = response.json()
    return info

# print(check_phone('9994492792'))