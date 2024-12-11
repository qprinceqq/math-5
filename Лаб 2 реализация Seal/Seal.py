class SimpleSEAL:
    def __init__(self, key: bytes, iv: bytes):
        """
        Инициализация SEAL с использованием ключа и IV.
        :param key: Ключ (20 байт или 160 бит).
        :param iv: Вектор инициализации (20 байт или 160 бит).
        """
        if len(key) != 20 or len(iv) != 20:
            raise ValueError("Ключ и IV должны быть длиной 20 байт (160 бит).")

        self.key = int.from_bytes(key, 'big')
        self.iv = int.from_bytes(iv, 'big')
        # Инициализация состояния (80-битное начальное значение)
        self.state = (self.key ^ self.iv) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    def generate_keystream(self, length: int) -> bytes:
        """
        Генерация ключевого потока.
        :param length: Длина ключевого потока (в байтах).
        :return: Ключевой поток в виде байтов.
        """
        keystream = bytearray()
        for _ in range(length):
            # Генерация состояния с использованием простейшего нелинейного обновления
            self.state = (self.state * 6364136223846793005 + 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            # Добавляем 1 байт из состояния в поток
            keystream.append((self.state >> 72) & 0xFF)  # Берем старший байт из состояния
        return bytes(keystream)

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Шифрование текста.
        :param plaintext: Открытый текст (байты).
        :return: Зашифрованный текст (байты).
        """
        keystream = self.generate_keystream(len(plaintext))
        ciphertext = bytes(pt ^ ks for pt, ks in zip(plaintext, keystream))
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Дешифрование текста.
        :param ciphertext: Зашифрованный текст (байты).
        :return: Открытый текст (байты).
        """
        return self.encrypt(ciphertext)  # XOR-шифрование симметрично


# Тестирование SimpleSEAL
if __name__ == "__main__":
    # 160-битный ключ и IV
    key = b"this_is_160_bit_key!"
    iv = b"00000000000000000000"

    plaintext = b"Hello, SEAL Encryption Algorithm!"
    print("Исходный текст:", plaintext)

    # Создаем объект SimpleSEAL
    seal = SimpleSEAL(key, iv)

    # Шифруем текст
    ciphertext = seal.encrypt(plaintext)
    print("Зашифрованный текст (в байтах):", ciphertext)

    # Расшифровываем текст
    decrypted_text = seal.decrypt(ciphertext)
    print("Расшифрованный текст (в байтах):", decrypted_text)

    # Проверяем, что расшифрованный текст совпадает с исходным
    if decrypted_text == plaintext:
        print("Расшифровка успешна.")
        print("Расшифрованный текст:", decrypted_text.decode("utf-8"))
    else:
        print("Ошибка: Расшифрованный текст не совпадает с исходным!")
