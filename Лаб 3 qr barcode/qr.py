import qrcode
from PIL import Image

# Создаем QR-код с высоким уровнем коррекции
data = "https://ru.pinterest.com/pin/287948969918793778/"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Высокая коррекция
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("original_qr.png")

# Имитируем повреждение изображения
img = Image.open("original_qr.png")
pixels = img.load()

# Удаляем часть данных
for i in range(150, 250):
    for j in range(150, 250):
        pixels[i, j] = 255
img.save("damaged_qr.png")
