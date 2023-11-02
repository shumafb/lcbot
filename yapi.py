import requests
import json

with open("source/info.json", "r", encoding="utf-8") as file:
    file = json.load(file)

YA_TOKEN = file["yandexl_token"]

RNC = {'1': 1651, '2': 233, '2046': 139, '2048': 106, '99': 1323}


# Формирование JSON

# Отправка POST-запроса
url = "https://api.lbs.yandex.net/geolocation"


def push_api(lac, cid, mnc):
    print(lac, cid, mnc)
    """Принимает lac, cid, mnc базовой станции,
    отправляет запрос Яндекс.Локатору
    и возвращает ответ"""
    print(cid)
    print(type(cid))
    print(mnc)
    if len(str(cid)) == 5:
        print('IF CID')
        if int(mnc) == 20 and cid[:2] == '48':
            cellid16 = f"{RNC['2048']:x}{int(cid):x}"
            print(cellid16)
            cid = int(cellid16, 16)
            print(cid)
        elif int(mnc) == 20 and cid[:2] == '46':
            cellid16 = f"{RNC['2046']:x}{imt(cid):x}"
            print(cellid16)
            cid = int(cellid16, 16)
            print(cid)
        elif int(mnc) == 1:
            print(mnc)
            cellid16 = f"{RNC['1']:x}{int(cid):x}"
            cid = int(cellid16, 16)
            print(cellid16)
            print(cid)
        elif int(mnc) == 2:
            cellid16 = f"{RNC['2']:x}{int(cid):x}"
            cid = int(cellid16, 16)
            print(cid)

    data = f'json={{"common": {{"version": "1.0", "api_key": "3335cce6-3e6b-443f-bfd9-ee6ed7689d62"}}, "gsm_cells": [ {{ "countrycode": 250, "operatorid": {mnc}, "cellid": {cid}, "lac": {lac}, "signal_strength": -80, "age": 1000}} ]}}'

    response = requests.post("http://api.lbs.yandex.net/geolocation", data=data)
    save_data = response.json()
    latitude = save_data["position"]["latitude"]
    longitude = save_data["position"]["longitude"]
    coord = str(latitude)[:9] + "-" + str(longitude)[:9]
    radius = save_data["position"]["precision"]
    # Проверка ответа
    if coord == '44.606681-40.105854':
        coord = '00.000000-00.000000'
    if response.status_code == 200:
        bsinfo = {"operator": mnc, "coord": coord, "radius": radius}
        return bsinfo

    else:
        return f"Ошибка: {response.status_code}, {response.text}"


def check_imei(imei):
    response = requests.get(f"https://alpha.imeicheck.com/api/modelBrandName?imei={imei}&format=json")
    if response.status_code == 200:
        x = response.json()['result'].split('<br>')[:-1]
        print(response.json())
        return x
    else:
        return f"Ошибка: {response.status_code}, {response.text}"
    