def luhn(imei_info):
    imei = list(str(imei_info))
    nch = imei[::2]
    ch = imei[1::2]
    double_ch = [str(int(x)*2) for x in ch]
    double_ch = list(''.join(double_ch))
    rch = sum(list(map(int, double_ch)))
    nrch = sum(list(map(int, nch)))
    result = (nrch + rch) % 10
    control = 10 - result
    full_imei = int(f"{imei_info}{control}")
    return full_imei