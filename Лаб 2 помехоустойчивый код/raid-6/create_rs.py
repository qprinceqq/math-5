from rs_functions import *

# Здесь представлены наши диски с данными о них.
image1 = [ord('f'), ord('i'), ord('r'), ord('s'), ord('t')]
image2 = [ord('s'), ord('e'), ord('c'), ord('n'), ord('d')]
image3 = [ord('t'), ord('h'), ord('i'), ord('r'), ord('d')]

# Это место для нашего диска RS. Он будет регенерирован в строках ниже.
imageRS = [0] * 5

# А это наш цикл, который генерирует данные RS, используя не более кроме дисков с данными пользователя.
for i in range(0, 5):
    imageRS[i] = gf_add(gf_mul(gf_drive(1), image1[i]),
                        gf_mul(gf_drive(2), image2[i]),
                        gf_mul(gf_drive(3), image3[i]))

dump_table("RS", imageRS)
