import hashlib
import time
from itertools import chain

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


def check_fio(fio):
    fio_hash = hashlib.md5(fio.lower().encode()).hexdigest()
    file = f"db/dbln/{fio_hash[0:1]}/{fio_hash[1:2]}/{fio_hash[0:4]}.csv"
    print(file)
    df = pd.read_csv(file, header=0).replace(np.nan, None)
    df_fil = df.loc[df['lnmatch_last_name'] == fio.lower()]

    return df_fil

def check_phone(phone):
    name = []  # Возможные имена
    yandex_address = []  # Адрес по яндекс еде по ячейкам
    doorcode = []  # код домофона
    delivery_address = []  # адрес по деливер
    beeline_address = []  # адрес по билайну
    sphone = str(phone)
    file = f"db/dbpn/{sphone[0:2]}/{sphone[2:4]}/{sphone[4:6]}/{sphone[6:8]}.csv"
    df = pd.read_csv(file, header=0).replace(np.nan, None)
    df_filter = df.loc[df["phone_number"] == phone]
    df_filter["yandex_address_full"] = (
        df_filter["yandex_address_city"].astype(str)
        + ", "
        + df_filter["yandex_address_street"].astype(str)
        + ", "
        + df_filter["yandex_address_house"].astype(str)
    )
    df_filter = df_filter.drop(
        columns=["yandex_address_city", "yandex_address_street", "yandex_address_house"]
    )
    unique_data = {"phone_number": df_filter["phone_number"].iloc[0]}
    for column in df_filter.columns:
        if column != "phone_number":
            unique_data[column] = list(df_filter[column].unique())
    result_df = pd.DataFrame([unique_data])
    return result_phone(result_df.to_dict())


def result_phone(result):
    for key, value in result.items():
        if key.endswith("name"):
            if key.endswith("vendor_name"):
                continue
            else:
                name.append(value[0])
        if key.startswith("yandex_address"):
            if (
                key.startswith("yandex_address_comment")
                or key.startswith("yandex_address_office")
                or key.startswith("yandex_address_entrance")
                or key.startswith("yandex_address_floor")
            ):
                continue
            elif key.startswith("yandex_address_doorcode") and value[0] not in doorcode:
                doorcode.append(value[0])
            elif key.startswith("yandex_address_full") and value[0] != None:
                yandex_address.append(value[0])
        if key.startswith("delivery2_address") and value[0] not in delivery_address:
            if key.startswith("delivery2_address_full"):
                delivery_address.append(value[0])
            elif (
                key.startswith("delivery2_address_intercom")
                and value[0] not in doorcode
            ):
                doorcode.append(value[0])
        if key.startswith("beeline_address_"):
            if key.startswith("beeline_address_entrance_count") or key.startswith("beeline_address_floors_count"):
                continue
            elif value[0] not in beeline_address:
                beeline_address.append(value[0])


    result_format = {
        "name": list(filter(lambda item: item is not None, list(set(list(chain(*name)))))),
        "doorcode": list(filter(lambda item: item is not None, list(set(list(chain(*doorcode)))))),
        "ya_deli_bee_address": list(filter(lambda item: item is not None, list(set(list(chain(*yandex_address, *delivery_address, *beeline_address)))))),
    }


    return result_format


x = 'байбеков'
print(check_fio(x))