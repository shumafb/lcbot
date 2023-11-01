import hashlib
import os
import glob
from itertools import chain
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


# SAVERU
def check_fio(fio):
    filter = None
    fio_list = fio.split()
    fio = fio_list[0].lower()
    fio_hash = hashlib.md5(fio.lower().encode()).hexdigest()
    if len(fio_list) > 1:
        filter = fio_list[1].lower()
    file = f"db/dbln/{fio_hash[0:1]}/{fio_hash[1:2]}/{fio_hash[0:4]}.csv"
    df = pd.read_csv(file, header=0).replace(np.nan, "")
    df = df.loc[df["lnmatch_last_name"] == fio.lower()]
    if filter is not None:
        df = df.loc[
            (df["wildberries_name"].apply(str.lower).str.contains(filter))
            | (df["rfcont_name"].apply(str.lower).str.contains(filter))
            | (df["vk_first_name"].apply(str.lower).str.contains(filter))
            | (df["gibdd2_base_name"].apply(str.lower).str.contains(filter))
            | (df["gibdd2_name"].apply(str.lower).str.contains(filter))
            | (df["cdek_full_name"].apply(str.lower).str.contains(filter))
            | (df["beeline_full_name"].apply(str.lower).str.contains(filter))
            | (df["fb_full_name"].apply(str.lower).str.contains(filter))
            | (df["avito_user_name"].apply(str.lower).str.contains(filter))
            | (df["yandex_name"].apply(str.lower).str.contains(filter))
            # | (df["mailru_full_name"].apply(str.lower).str.contains(filter))
            | (df["delivery2_name"].apply(str.lower).str.contains(filter))
            | (df["gibdd_name"].apply(str.lower).str.contains(filter))
        ]
    # Работа со столбцом адрес яндекс
    df["yandex_address_full"] = (
        df["yandex_address_city"].astype(str)
        + ", "
        + df["yandex_address_street"].astype(str)
        + ", "
        + df["yandex_address_house"].astype(str)
    )
    df.drop(
        columns=["yandex_address_city", "yandex_address_street", "yandex_address_house"]
    )

    #   Работа со столбцом адрес билайн
    df["beeline_address_full"] = (
        df["beeline_address_city"].astype(str)
        + ", "
        + df["beeline_address_street"].astype(str)
        + ", "
        + df["beeline_address_house"].astype(str)
    )
    df.drop(
        columns=[
            "beeline_address_city",
            "beeline_address_street",
            "beeline_address_house",
        ]
    )

    # Работа с авто гибдд
    df["gibdd2_car_full"] = (
        df["gibdd2_car_model"].astype(str)
        + ", "
        + df["gibdd2_car_year"].astype(str)
        + ", "
        + df["gibdd2_car_vin"].astype(str)
        + ", "
        + df["gibdd2_car_color"].astype(str)
    )
    df.drop(
        columns=[
            "gibdd2_car_model",
            "gibdd2_car_year",
            "gibdd2_car_vin",
            "gibdd2_car_color",
        ]
    )
    if df.empty:
        print("YESS111")
        return {"status": 0, "result": "Нет данных"}
    elif df.shape[0] == 1:
        result = df.reset_index(drop=True)
        return {"status": 1, "result": result_fio(result).to_dict()}
    elif df.shape[0] <= 10:
        result = df.reset_index(drop=True)
        return {"status": 2, "result": result_fio(result).to_dict()}
    elif df.shape[0] > 10:
        result = df.reset_index(drop=True)
        result = result_fio(result).to_csv("result.csv", index=False)
        return {"status": 3, "result": result}


def result_fio(result):
    result_list = []
    result = result.to_dict()
    for i in range(len(result["lnmatch_last_name"])):
        name = []  # Имена
        phone_number = []  # Номера телефонов
        birthday_list = []  # Дата рождения
        address_list = []  # Адреса
        email_list = []  # Email
        car_list = []  # Авто
        car_plate_list = []  # Госномера
        for key, value in result.items():
            if key.endswith("name"):
                if (
                    key.startswith("okrug_nameokrug")
                    or key.startswith("yandex_place_name")
                    or key.endswith("vendor_name")
                    or key.startswith("delivery_name")
                    or key.startswith("miltor_name")
                    or key.startswith("pikabu_username")
                ):
                    continue
                elif key.startswith("lnmatch_last_name"):
                    name.append([value[i]])
                else:
                    name.append([value[i]])
            if key.startswith("phone_number"):
                phone_number.append([str(value[i])])
            if (
                key.endswith("address_full")
                or key.startswith("wildberries_address")
                or key.startswith("gibdd2_passport_address")
                or key.startswith("gibdd2_address")
            ):
                address_list.append([value[i]])
            if key.endswith("email"):
                email_list.append([value[i]])
            if key.endswith("plate_number"):
                car_plate_list.append([value[i]])
            if key.startswith("gibdd2_car_full"):
                car_list.append([value[i]])
            if key.endswith("birth"):
                birthday_list.append([value[i]])
        result_format = {
            "name": ", ".join(
                list(
                    filter(lambda item: item is not None, list(set(list(chain(*name)))))
                )
            ),
            "phone_number": ", ".join(
                list(
                    filter(
                        lambda item: item is not None,
                        list(set(list(chain(*phone_number)))),
                    )
                )
            ),
            "birthday_list": ", ".join(
                list(
                    filter(
                        lambda item: item is not None,
                        list(set(list(chain(*birthday_list)))),
                    )
                )
            ),
            "address_list": ", ".join(
                list(
                    filter(
                        lambda item: item is not None,
                        list(set(list(chain(*address_list)))),
                    )
                )
            ),
            "email_list": ", ".join(
                list(
                    filter(
                        lambda item: item is not None,
                        list(set(list(chain(*email_list)))),
                    )
                )
            ),
            "car_list": ", ".join(
                list(
                    filter(
                        lambda item: item is not None, list(set(list(chain(*car_list))))
                    )
                )
            ),
            "car_plate_list": ", ".join(
                list(
                    filter(
                        lambda item: item is not None,
                        list(set(list(chain(*car_plate_list)))),
                    )
                )
            ),
        }
        for key, value in result_format.items():
            result_format[key] = (
                value.replace(", ,", "")
                .replace(" , ", "")
                .replace(" ,", "")
                .replace("  ", "")
            )
        result_list.append(result_format)

    return pd.DataFrame(result_list)


def check_phone(phone):
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
    try:
        unique_data = {"phone_number": phone}
    except IndexError:
        unique_data = None

    for column in df_filter.columns:
        if column != "phone_number":
            unique_data[column] = list(df_filter[column].unique())
    result_df = pd.DataFrame([unique_data])
    return result_phone(result_df.to_dict())


def result_phone(result):
    name = []  # Возможные имена
    yandex_address = []  # Адрес по яндекс еде по ячейкам
    doorcode = []  # код домофона
    delivery_address = []  # адрес по деливер
    beeline_address = []  # адрес по билайну
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
            elif key.startswith("yandex_address_full") and value[0] is not None:
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
            if key.startswith("beeline_address_entrance_count") or key.startswith(
                "beeline_address_floors_count"
            ):
                continue
            elif value[0] not in beeline_address:
                beeline_address.append(value[0])

    result_format = {
        "name": list(
            filter(lambda item: item is not None, list(set(list(chain(*name)))))
        ),
        "doorcode": list(
            filter(lambda item: item is not None, list(set(list(chain(*doorcode)))))
        ),
        "ya_deli_bee_address": list(
            filter(
                lambda item: item is not None,
                list(
                    set(
                        list(
                            chain(*yandex_address, *delivery_address, *beeline_address)
                        )
                    )
                ),
            )
        ),
    }
    return result_format


# Sliv


def check_sliv(fio=None, phone=None, flag=None):
    filter = None
    if fio != None:
        cursor = fio.strip().lower()
        flag = "fio"
    elif phone != None:
        cursor = phone[-10:]
        flag = "phone"
    directory = "db/sliv/*"
    files = [os.path.abspath(f) for f in glob.glob(directory)]
    for file in files:
        info = {}
        if file.endswith("xlsx" or "xls"):
            print("EXCEL")
            df = pd.read_excel(file, header=0)
        elif file.endswith("csv"):
            print("CSV")
            df = pd.read_csv(file, header=0)
        df['phone'] = df['phone'].str[-10:]
        try:
            if flag == "fio":
                df = df.loc[df['fio'].str.lower() == cursor]
                info[f"{file[file.find('/sliv')+6:file.index('.')]}"] = df.reset_index(drop=True).to_dict()
                print(info)
            elif flag == "phone":
                df = df.loc[df["phone"] == cursor]
                info[f"{file[file.find('/sliv')+6:file.index('.')]}"] = df.reset_index(drop=True).to_dict()
        except KeyError:
            pass
        return info


# check_sliv(fio='Яцковец Галина Викторовна')
print(check_sliv(phone='Яцковец Галина Викторовна'))