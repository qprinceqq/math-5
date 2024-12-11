# Импорт numpy для работы с массивами
import numpy as np

# Параметры конечного поля
PRIMITIVE_POLY = 0b10011  # x^4 + x + 1
FIELD_SIZE = 2**4        # GF(2^4)

# Вычисление значения многочлена в точке
def evaluate_poly(poly, x, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    result = 0
    for coeff in poly:
        result = gf_mul(result, x, primitive_poly, field_size) ^ coeff
    return result


# Умножение в конечном поле
def gf_mul(a, b, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & field_size:
            a ^= primitive_poly
        b >>= 1
    return result

# Возведение в степень в конечном поле
def gf_pow(a, power, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    result = 1
    for _ in range(power):
        result = gf_mul(result, a, primitive_poly, field_size)
    return result

# Деление в конечном поле
def gf_div(a, b, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    if b == 0:
        raise ZeroDivisionError("Division by zero in GF")
    inv_b = gf_pow(b, field_size - 2, primitive_poly, field_size)  # Обратное значение
    return gf_mul(a, inv_b, primitive_poly, field_size)

def gf_add(a, b):
    return a ^ b

def generate_generator_polynomial(t, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    g = [1]
    for i in range(t):
        g = np.polymul(g, [1, gf_pow(2, i, primitive_poly, field_size)]).astype(int).tolist()
    return [coeff % field_size for coeff in g]

def encode_message(message, n, k, generator_poly, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    message_poly = [m % field_size for m in message]
    message_poly += [0] * (n - k)  # Дополнить до длины n
    remainder = np.polydiv(message_poly, generator_poly)[1]
    remainder = [int(r) % field_size for r in remainder]
    codeword = message_poly[:k] + remainder
    return codeword

def calculate_syndromes(received, t, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    syndromes = []
    for i in range(2 * t):
        syndromes.append(evaluate_poly(received, gf_pow(2, i, primitive_poly, field_size)))
    return syndromes


def correct_errors(received, syndromes, t, primitive_poly=PRIMITIVE_POLY, field_size=FIELD_SIZE):
    # Шаг 1: Алгоритм Берлекэмпа-Мэсси для нахождения полинома ошибок
    L = 0  # Степень текущего полинома ошибок
    C = [1]  # Текущий полином ошибок (начинаем с 1)
    B = [1]  # Дополнительный полином для вычислений
    sigma = [0] * (2 * t)  # Место для синдромов

    for i in range(2 * t):
        sigma[i] = syndromes[i]

    # Шаг 2: Итерации для нахождения полинома ошибок
    for i in range(2 * t):
        delta = syndromes[i]

        # Вычисление дельты
        for j in range(1, L + 1):
            delta ^= gf_mul(C[j], syndromes[i - j], primitive_poly, field_size)

        if delta != 0:
            # Переход на новый полином ошибок
            if 2 * L <= i:
                tmp = C[:]
                C = [gf_add(C[j], B[j]) for j in range(len(B))]  # Сложение полиномов
                L = i + 1 - L
                B = tmp
            C = [gf_add(C[j], [0] * (i - len(C)) + [delta])[j] for j in range(len(C))]

        # Обновление синдромов
        for j in range(L):
            syndromes[i + j] ^= gf_mul(C[j], delta, primitive_poly, field_size)

    # Шаг 3: Находим местоположения ошибок
    errors_pos = []
    for i in range(len(syndromes)):
        if evaluate_poly(C, gf_pow(2, i, primitive_poly, field_size)) == 0:
            errors_pos.append(i)

    # Исправление ошибок
    for pos in errors_pos:
        received[pos] ^= 1  # Корректируем ошибку на найденной позиции

    return received


# Параметры кода (n, k) и t
n = 15
k = 9
t = (n - k) // 2

# Сообщение для кодирования
message = [11, 13, 9, 6, 7, 15, 14, 12, 10]

# Генерация порождающего многочлена
generator_poly = generate_generator_polynomial(t)

# Кодирование
encoded_message = encode_message(message, n, k, generator_poly)
print("Закодированное сообщение:", encoded_message)

# Пример получения поврежденного сообщения
received_message = encoded_message.copy()
received_message[2] ^= 5  # Ошибка в одном символе
print("Полученное сообщение с ошибкой:", received_message)

# Вычисление синдромов
syndromes = calculate_syndromes(received_message, t)
print("Синдромы:", syndromes)

# Исправление ошибок
corrected_message = correct_errors(received_message, syndromes, t, generator_poly)
print("Исправленное сообщение:", corrected_message)
