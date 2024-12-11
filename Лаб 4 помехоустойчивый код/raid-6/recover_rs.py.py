from rs_functions import *

# Here are our drives, together with their data.
image1 = [ord('A'), ord('A'), ord('A'), ord('A'), ord('A')]
image2 = [ord('s'), ord('e'), ord('c'), ord('n'), ord('d')]
image3 = [ord('t'), ord('h'), ord('i'), ord('r'), ord('d')]

# This is a placeholder for our RS drive. It will be regenerated
# in the lines below.
imageRS = [0] * 5

# And this is our loop that generates the RS data using nothing more
# than the user data drives.
for i in range(0, 5):
    imageRS[i] = gf_add(gf_mul(gf_drive(1), image1[i]),
                        gf_mul(gf_drive(2), image2[i]),
                        gf_mul(gf_drive(3), image3[i]))

dump_table("imageRS", imageRS)
