import requests
import json

with open("source/info.json", "r", encoding="utf-8") as file:
    file = json.load(file)

YA_TOKEN = file["yandexl_token"]

# Формирование JSON

# Отправка POST-запроса
url = "https://api.lbs.yandex.net/geolocation"


def push_api(lac, cid, mnc):
    """Принимает lac, cid, mnc базовой станции,
    отправляет запрос Яндекс.Локатору
    и возвращает ответ"""
    data = f'json={{"common": {{"version": "1.0", "api_key": "3335cce6-3e6b-443f-bfd9-ee6ed7689d62"}}, "gsm_cells": [ {{ "countrycode": 250, "operatorid": {mnc}, "cellid": {cid}, "lac": {lac}, "signal_strength": -80, "age": 1000}} ]}}'

    response = requests.post("http://api.lbs.yandex.net/geolocation", data=data)

    save_data = response.json()
    latitude = save_data["position"]["latitude"]
    longitude = save_data["position"]["longitude"]
    coord = str(latitude)[:9] + "-" + str(longitude)[:9]
    radius = save_data["position"]["precision"]
    # Проверка ответа
    if response.status_code == 200:
        # return(response.json())
        # return(f"Координаты базовой станции {lac}-{cid}: {latitude} {longitude}, радиус - {radius}")

        bsinfo = {"operator": mnc, "coord": coord, "radius": radius}
        return bsinfo

    else:
        return f"Ошибка: {response.status_code}, {response.text}"


def check_imei(imei):
    response = requests.get(f"https://alpha.imeicheck.com/api/modelBrandName?imei={imei}&format=json")
    print(response)
    if response.status_code == 200:
        x = response.json()['result'].split('<br>')[:-1]
        print(response.json())
        return x
    else:
        return f"Ошибка: {response.status_code}, {response.text}"