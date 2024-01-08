def validate_iin(iin: str) -> bool:
    if len(iin) != 12:
        return False
    if iin[2:4] > "12" or iin[2:4] < "01":
        return False
    if iin[4:6] > "31" or iin[4:6] < "01":
        return False
    return True


def validate_ikt(ikt: str) -> bool:
    if len(ikt) != 9:
        return False
    return True


def validate_year(year: str) -> bool:
    if len(year) != 4:
        return False
    if int(year) < 2000:
        return False
    return True
