from gflog_tables import *


# Сложение
def gf_add(*args):
    result = 0
    for arg in args:
        result ^= arg

    return result


# Индексация
# Первый диск - 1, второй - 2, и т.д.
def gf_drive(index):
    global gfilog

    return gfilog[index - 1]


# Умножение
def gf_mul(a, b):
    global gflog
    global gfilog

    if a == 0 or b == 0:
        return 0
    else:
        return gfilog[(gflog[a] + gflog[b]) % 255]


# Помощник делителя
def sub_gf8(a, b):
    if a > b:
        return a - b
    else:
        return (255 - (0 - (a - b)))


# Деление
def gf_div(a, b):
    global gfilog
    global gflog

    return gfilog[sub_gf8(gflog[a], gflog[b])]
