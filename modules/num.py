import requests

url = "http://num.voxlink.ru/get/?num=+7"


def check_phone(phone):
    response = requests.get(url=url+phone)
    info = response.json()
    return info
