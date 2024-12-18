import os
import heapq
from collections import defaultdict


# Создание узла для алгоритма Хаффмана
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Построение дерева Хаффмана
def build_huffman_tree(data):
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1

    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


# Создание кодов Хаффмана
def build_huffman_codes(node, code="", codes={}):
    if node:
        if node.char:
            codes[node.char] = code
        build_huffman_codes(node.left, code + "0", codes)
        build_huffman_codes(node.right, code + "1", codes)
    return codes


# Сжатие данных методом Хаффмана
def huffman_compress(data):
    root = build_huffman_tree(data)
    huffman_codes = build_huffman_codes(root)
    compressed_data = ''.join(huffman_codes[char] for char in data)
    return compressed_data, huffman_codes


# Метод RLE
def rle_compress(data):
    compressed_data = []
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            compressed_data.append(data[i - 1] + str(count))
            count = 1
    compressed_data.append(data[-1] + str(count))
    return ''.join(compressed_data)


# Метод сжатия методом подстановки (LZ78)
def lz78_compress(data):
    dictionary = {}
    compressed_data = []
    current_string = ""
    dict_size = 1

    for char in data:
        combined = current_string + char
        if combined in dictionary:
            current_string = combined
        else:
            if current_string:
                compressed_data.append((dictionary[current_string], char))
            else:
                compressed_data.append((0, char))
            dictionary[combined] = dict_size
            dict_size += 1
            current_string = ""

    if current_string:
        compressed_data.append((dictionary[current_string], ""))

    return compressed_data


# Энтропийный метод: Арифметическое кодирование (простой пример)
def arithmetic_compress(data):
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1

    total = sum(freq.values())
    prob_ranges = {}
    low = 0.0

    for char, count in sorted(freq.items()):
        high = low + count / total
        prob_ranges[char] = (low, high)
        low = high

    low, high = 0.0, 1.0
    for char in data:
        range_low, range_high = prob_ranges[char]
        range_width = high - low
        high = low + range_width * range_high
        low = low + range_width * range_low

    return (low + high) / 2, prob_ranges


# Вычисление эффективности и коэффициента сжатия
def calculate_metrics(original_size, compressed_size):
    efficiency = original_size / compressed_size
    compression_ratio = (original_size - compressed_size) / original_size
    return efficiency, compression_ratio


# Основной скрипт
if __name__ == "__main__":
    # filename = input("Введите имя файла для сжатия: ")
    filename = "text.txt"

    if not os.path.isfile(filename):
        print("Ошибка: Файл не найден.")
        exit(1)

    with open(filename, "r") as file:
        original_text = file.read()

    original_size = len(original_text) * 8  # в битах

    print("Выберите метод сжатия:")
    print("1. Хаффман")
    print("2. RLE")
    print("3. Арифметическое кодирование")
    print("4. LZ78")


    choice = input("Введите номер метода: ")

    if choice == "1":
        compressed_data, _ = huffman_compress(original_text)
        compressed_size = len(compressed_data)
    elif choice == "2":
        compressed_data = rle_compress(original_text)
        compressed_size = len(compressed_data) * 8
    elif choice == "4":
        compressed_data = lz78_compress(original_text)
        compressed_size = sum(len(str(index)) + len(char) for index, char in compressed_data) * 8
    elif choice == "3":
        compressed_data, _ = arithmetic_compress(original_text)
        compressed_size = len(str(compressed_data)) * 8
    else:
        print("Неверный выбор метода сжатия.")
        exit(1)

    efficiency, compression_ratio = calculate_metrics(original_size, compressed_size)

    print("\nРезультаты:")
    print(f"Исходный текст: {original_text}")
    print(f"Сжатый текст: {compressed_data}")
    print(f"Эффективность сжатия: {efficiency:.2f}")
    print(f"Коэффициент сжатия: {compression_ratio:.2%}")

    with open(f"{filename}.compressed", "w") as output_file:
        output_file.write(str(compressed_data))

    print(f"\nСжатые данные сохранены в файл: {filename}.compressed")
