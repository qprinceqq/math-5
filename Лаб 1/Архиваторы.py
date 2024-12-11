import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import heapq


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


# Логирование запросов
def log_request(request_num, text, ratio_huffman, ratio_rle, e_huffman):
    log_entry = f"№{request_num} | Текст: {text} | Эф. хаффмана{e_huffman:.2f} | Коэф. Хаффмана{ratio_huffman:.2f} | Коэф. RLE{ratio_rle:.2f}\n"
    with open("compression_log.txt", "a") as f:
        f.write(log_entry)


# Приложение на tkinter
class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сравнение методов сжатия данных")
        self.request_count = 0

        # Ввод текста
        self.input_label = tk.Label(root, text="Введите текст для сжатия:")
        self.input_label.pack()
        self.text_entry = tk.Entry(root, width=50)
        self.text_entry.insert(0, "AAAAAAAAffff")
        self.text_entry.pack()

        # Кнопка для запуска
        self.compress_button = tk.Button(root, text="Сжать и сравнить", command=self.compress_text)
        self.compress_button.pack()

        # Результаты
        self.result_label = tk.Label(root, text="Результаты сжатия")
        self.result_label.pack()
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack()

    def compress_text(self):
        # Получаем текст
        text = self.text_entry.get()
        if not text:
            messagebox.showerror("Ошибка", "Введите текст для сжатия!")
            return

        # Сжатие методами Хаффмана и RLE
        compressed_huffman, huffman_codes = huffman_compress(text)
        compressed_rle = rle_compress(text)

        e_huffman = len(text) * 8 / len(compressed_huffman)
        # Вычисление коэффициентов сжатия
        ratio_huffman = len(text) / len(compressed_huffman)
        ratio_rle = len(text) / len(compressed_rle)

        # Вывод результатов
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END,
                                f"Метод Хаффмана:\n{compressed_huffman}\nЭффективность сжатия: {e_huffman:.2f}\nКоэффициент сжатия: {ratio_huffman:.2f}\n\n")
        self.result_text.insert(tk.END, f"Метод RLE:\n{compressed_rle}\nКоэффициент сжатия: {ratio_rle:.2f}\n")

        # Логирование
        self.request_count += 1
        log_request(self.request_count, text, ratio_huffman, ratio_rle, e_huffman)


# Создание интерфейса
root = tk.Tk()
app = CompressionApp(root)
root.mainloop()
