import hashlib
import time

import numpy as np
import pandas as pd

name = []  # Возможные имена
yandex_address = []  # Адрес по яндекс еде по ячейкам
doorcode = []  # код домофона
delivery_address = []  # адрес по деливер
beeline_address = []  # адрес по билайну
result = []

def check_fio(fio):
    fio_hash = hashlib.md5(fio.lower().encode()).hexdigest()
    file = f"db/dbln/{fio_hash[0:1]}/{fio_hash[1:2]}/{fio_hash[0:4]}.csv"
    df = pd.read_csv(file, header=0).replace(np.nan, None)


def check_phone(phone):
    sphone = str(phone)
    file = f"db/dbpn/{sphone[0:2]}/{sphone[2:4]}/{sphone[4:6]}/{sphone[6:8]}.csv"
    df = pd.read_csv(file, header=0).replace(np.nan, None)
    card_list = []
    for row in df.iterrows():
        card = row[1].to_dict()
        if phone == card["phone_number"]:
            card_list.append(card)
    print(len(card_list))
    for card in card_list:
        for key, value in card.items():
            print(value) 
            # for key, value in card.items():
            #     if value != None:
            #         pretty_card[key] = value
            

    # return result


# def result_phone(pretty_card):
#     for key, value in pretty_card.items():
#         # ya_city = None # Город
#         # ya_street = None # Улица
#         # ya_house = None # Дом
#         ya_address = str()
#         if key.endswith("name"):
#             if key.endswith("vendor_name"):
#                 continue
#             else:
#                 name.append(value)
#         if key.startswith("yandex_address"):
#             if (
#                 key.startswith("yandex_address_comment")
#                 or key.startswith("yandex_address_office")
#                 or key.startswith("yandex_address_entrance")
#                 or key.startswith("yandex_address_floor")
#             ):
#                 continue
#             elif key.startswith("yandex_address_doorcode") and value not in doorcode:
#                 doorcode.append(str(value))
#             elif key.startswith("yandex_address_city") and value != None:
#                 ya_address = str(value)+', '
#             elif key.startswith("yandex_address_street") and value != None:
#                 ya_address += str(value)+', '
#             elif key.startswith("yandex_address_house") and value != None:
#                 ya_address += str(value)+', '
#         if key.startswith("delivery2_address") and value not in delivery_address:
#             if key.startswith("delivery2_address_full"):
#                 delivery_address.append(str(value))
#             elif key.startswith("delivery2_address_intercom") and value not in doorcode:
#                 doorcode.append(str(value))
#         if key.startswith("beeline_address_"):
#             if key.startswith("beeline_address_entrance_count") or key.startswith("beeline_address_floors_count"):
#                 continue
#             elif value not in beeline_address:
#                 beeline_address.append(str(value))
    
#     yandex_address.append(ya_address)
#     return {
#         'name': set(name),
#         'doorcode': set(doorcode),
#         'yandex_address': set(yandex_address),
#         'delivery_address': set(delivery_address),
#         'beeline_address': set(beeline_address),
#     }


phone = 79953201443
x = check_phone(phone)
print(x)