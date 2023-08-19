import requests

YA_TOKEN = "3335cce6-3e6b-443f-bfd9-ee6ed7689d62"

# Формирование JSON

# Отправка POST-запроса
url = "https://api.lbs.yandex.net/geolocation"


def push_api(lac, cid, mnc):
    data = f'json={{"common": {{"version": "1.0", "api_key": "3335cce6-3e6b-443f-bfd9-ee6ed7689d62"}}, "gsm_cells": [ {{ "countrycode": 250, "operatorid": {mnc}, "cellid": {cid}, "lac": {lac}, "signal_strength": -80, "age": 1000}} ]}}'

    response = requests.post('http://api.lbs.yandex.net/geolocation', data=data)


    save_data = response.json()
    latitude = save_data['position']['latitude']
    longitude = save_data['position']['longitude']
    radius = save_data['position']['precision']
    # Проверка ответа
    if response.status_code == 200:
        # return(response.json())
        return(f"Координаты базовой станции {lac}-{cid}: {latitude} {longitude}, радиус - {radius}")
    else:
        return(f"Ошибка: {response.status_code}, {response.text}")