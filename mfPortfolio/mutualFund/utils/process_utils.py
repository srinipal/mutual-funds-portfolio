def strip_off_new_line(str_val):
    if str_val is not None:
        return str_val.split("\n")[0].strip()
    return None


def parse_percent(str_val):
    if str_val is None:
        return None
    if "-" == str_val:
        return None
    return float(str_val.strip('%'))/100.0


def parse_currency_val(currency_val):
    if currency_val is None:
        return None
    if "-" == currency_val:
        return None
    multiplication_factor = 1
    currency_val_comps = currency_val.split(" ")
    if len(currency_val_comps) == 2:
        currency_qty = currency_val_comps[1].lower()
        if "cr" == currency_qty:
            multiplication_factor = 10000000
        elif "l" == currency_qty:
            multiplication_factor = 100000
        elif "k" == currency_qty:
            multiplication_factor = 1000
        else:
            raise Exception('unrecognised currency qty: ' + str(currency_qty))

    return float(currency_val_comps[0].replace(',', '')) * multiplication_factor
