from PIL import Image, ImageDraw


def generate_ean13_barcode(data):
    if len(data) != 12 or not data.isdigit():
        raise ValueError("Данные должны содержать 12 цифр.")

    def calculate_checksum(data):
        odd_sum = sum(int(data[i]) for i in range(0, len(data), 2))
        even_sum = sum(int(data[i]) for i in range(1, len(data), 2))
        return (10 - (odd_sum + 3 * even_sum) % 10) % 10

    data += str(calculate_checksum(data))
    patterns = {
        '0': "0001101", '1': "0011001", '2': "0010011", '3': "0111101",
        '4': "0100011", '5': "0110001", '6': "0101111", '7': "0111011",
        '8': "0110111", '9': "0001011"
    }
    # Создаем штрих-код из шаблонов.
    code = "101"  # Стартовый разделитель
    for i, digit in enumerate(data[:7]):
        code += patterns[digit]
    code += "01010"  # Разделитель середины
    for digit in data[7:]:
        code += patterns[digit]
    code += "101"  # Конечный разделитель

    # Рисуем изображение.
    width, height = len(code), 100
    img = Image.new("1", (width, height), 1)  # Белый фон
    draw = ImageDraw.Draw(img)
    for i, bit in enumerate(code):
        if bit == "1":
            draw.line([(i, 0), (i, height)], fill=0)
    img.show()
    img.save("barcode.png")


# Пример использования
generate_ean13_barcode("123456789012")
