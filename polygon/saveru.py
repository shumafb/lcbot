import pandas as pd
import numpy as np
import hashlib
import time


def check_fio(fio):
    fio_hash = hashlib.md5(fio.lower().encode()).hexdigest()
    file = f"db/dbln/{fio_hash[0:1]}/{fio_hash[1:2]}/{fio_hash[0:4]}.csv"
    df = pd.read_csv(file, header=0).replace(np.nan, None)




def check_phone(phone):
    sphone = str(phone)
    file = f"db/dbpn/{sphone[0:2]}/{sphone[2:4]}/{sphone[4:6]}/{sphone[6:8]}.csv"
    df = pd.read_csv(file, header=0).replace(np.nan, None)
    for row in df.iterrows():
        card = row[1].to_dict()
        if phone == card['phone_number']:
            print(card)





phone = 79953201172
check_phone(phone)