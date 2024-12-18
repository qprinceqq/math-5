from rs_functions import *

# Что уцелело
image1 = [ord('f'), ord('i'), ord('r'), ord('s'), ord('t')]
imagePD = [0x61, 0x64, 0x78, 0x6f, 0x74]
imageRS = [0x4d, 0x1e, 0x0d, 0x7a, 0x31]

# Что пропало
image2 = [0] * 5
image3 = [0] * 5

for i in range(0, 5):
    partialRS = gf_add(gf_mul(gf_drive(1), image1[i]))

    xoredPD = gf_add(image1[i], imagePD[i])
    xoredRS = gf_add(partialRS, imageRS[i])
    mid = gf_add(gf_mul(gf_drive(3), xoredPD), xoredRS)

    # Восстанавливаем D2.
    data = gf_mul(mid, gf_div(1, gf_add(gf_drive(2), gf_drive(3))))
    image2[i] = data

    # Восстанавливаем D3.
    image3[i] = gf_add(image1[i], image2[i], imagePD[i])


dump_table("image2", image2)
dump_table("image3", image3)
