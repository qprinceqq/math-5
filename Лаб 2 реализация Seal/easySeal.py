class SEAL:
    def __init__(self, key: int, iv: int):
        """
        Инициализация SEAL с ключом и вектором инициализации.
        :param key: 64-битный ключ (целое число)
        :param iv: 64-битный вектор инициализации
        """
        self.initial_state = (key ^ iv) & 0xFFFFFFFFFFFFFFFF  # Начальное состояние генератора
        self.state = self.initial_state  # Текущее состояние

    def reset(self):
        """
        Сбрасывает генератор ключевого потока в начальное состояние.
        """
        self.state = self.initial_state

    def next_key_byte(self):
        """
        Генерация следующего байта ключевого потока с помощью Linear Congruential Generator (LCG).
        """
        # Константы LCG
        a = 6364136223846793005  # Множитель
        c = 1  # Приращение
        m = 2**64  # Модуль
        self.state = (a * self.state + c) % m
        return self.state & 0xFF  # Возвращаем младший байт

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Шифрование текста путем XOR с ключевым потоком.
        :param plaintext: Байтовая строка открытого текста
        :return: Байтовая строка зашифрованного текста
        """
        self.reset()  # Сбрасываем генератор ключей
        encrypted = bytearray()
        for byte in plaintext:
            encrypted.append(byte ^ self.next_key_byte())
        return bytes(encrypted)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Дешифрование текста. Процесс идентичен шифрованию.
        :param ciphertext: Байтовая строка зашифрованного текста
        :return: Байтовая строка расшифрованного текста
        """
        return self.encrypt(ciphertext)  # XOR-шифрование симметрично


# Тестирование SEAL
if __name__ == "__main__":
    # Определяем ключ и вектор инициализации
    key = 0x1234567890ABCDEF  # 64-битный ключ
    iv = 0x0000000000000000  # 64-битный IV
    plaintext = b"Hello, SEAL Encryption!"  # Текст для шифрования

    print("Исходный текст:", plaintext)

    # Создаем объект SEAL
    seal = SEAL(key, iv)

    # Шифруем текст
    ciphertext = seal.encrypt(plaintext)
    print("Зашифрованный текст (в байтах):", ciphertext)

    # Расшифровываем текст
    decrypted_text = seal.decrypt(ciphertext)
    print("Расшифрованный текст", decrypted_text)

    # Проверяем, что расшифрованный текст совпадает с исходным
    if decrypted_text == plaintext:
        print("Расшифровка успешна.")
    else:
        print("Ошибка: Расшифрованный текст не совпадает с исходным!")
