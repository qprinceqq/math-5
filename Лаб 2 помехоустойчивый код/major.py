import random

def replicate_data(data, n):
    """
    Функция для репликации данных.

    :param data: Исходные данные (строка).
    :param n: Число реплик.
    :return: Список реплик данных.
    """
    return [data] * n


def detect_and_correct(replicas):
    """
    Функция для обнаружения и исправления ошибок в репликах.

    :param replicas: Список реплик данных.
    :return: Исправленные данные.
    """
    from collections import Counter

    # Преобразуем список реплик в список символов (поколоночно)
    columns = zip(*replicas)

    # Для каждой позиции находим наиболее часто встречающийся символ
    corrected_data = "".join(Counter(column).most_common(1)[0][0] for column in columns)

    return corrected_data


def text_to_binary(text):
    binary_representation = ''.join(format(ord(char), '08b') for char in text)
    return binary_representation


def binary_to_text(binary_str):
    characters = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    text = ''.join(chr(int(char, 2)) for char in characters)
    return text


# Исходные данные
original_data = "OKOLO POD NAD PRI V"
binary_data = text_to_binary(original_data)
print("Изначальное сообщение:", original_data)

# Число реплик
num_replicas = 8

# Генерируем реплики данных
replicas = replicate_data(binary_data, num_replicas)

# Имитируем ошибку в нескольких репликах
for i in range(3):
    rand = random.randint(1, len(binary_data))
    replicas[i] = '0' * rand + binary_data[rand:]

print("Реплики данных:")
for i, replica in enumerate(replicas):
    print(f"Реплика {i + 1}: {replica}")

# Обнаружение и исправление ошибок
corrected_data = detect_and_correct(replicas)

print("\nИсправленные данные:")
print(corrected_data)
print(binary_to_text(corrected_data))
