KILO = 1000
MEGA = KILO * KILO
GIGA = MEGA * KILO
TERA = GIGA * KILO
PETA = TERA * KILO
EXA = PETA * KILO


def convert_size(size: int):
    if size < 0:
        return ""
    elif size < KILO:
        return f'{size}B'
    elif size < MEGA:
        return f'{round(size / 1000, 2)}KB'
    elif size < GIGA:
        return f'{round(size / 1000 / 1000, 2)}MB'
    elif size < TERA:
        return f'{round(size / 1000 / 1000 / 1000, 2)}GB'
    elif size < PETA:
        return f'{round(size / 1000 / 1000 / 1000 / 1000, 2)}TB'
    elif size < EXA:
        return f'{round(size / 1000 / 1000 / 1000 / 1000 / 1000, 2)}PB'
    else:
        return f'{round(size / 1000 / 1000 / 1000 / 1000 / 1000 / 1000, 2)}EB'


def convert_millis(millis):
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    days = (millis / (1000 * 60 * 60 * 24)) % 7
    days = int(days)
    return seconds, minutes, hours, days


def convert_millis_to_string(millis) -> str:
    seconds, minutes, hours, days = convert_millis(millis)
    return f'{days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds'


def isBlank(s: str) -> bool:
    if s:
        if not s.strip():
            return True
        else:
            return False
    return False
