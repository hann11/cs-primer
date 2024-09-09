with open("teapot.bmp", "rb") as f:
    original_bmp = f.read()

# print the first 2 bytes
bm_header = original_bmp[:2]
size_bmp = original_bmp[2:6]
res_1 = original_bmp[6:8]
res_2 = original_bmp[8:10]
offset = original_bmp[10:14]  # in little endian
width = original_bmp[18:22]  # in little endian
height = original_bmp[22:26]  # in little endian

print(f"{bm_header=}")
print(f"{size_bmp=}")
print(f"{res_1=}")
print(f"{res_2=}")
print(f"{offset=}")


def convert_le_to_int(byte_input: bytes) -> int:
    """
    Convert little endian bytes to int
    """
    num = 0

    for b in reversed(byte_input):
        num <<= 8
        num |= b

    return num


# convert size_bmp to int, it's little endian
size_bmp_int = convert_le_to_int(size_bmp)

# convert offset to int, it's little endian
offset_int = convert_le_to_int(offset)

width_int = convert_le_to_int(width)
height_int = convert_le_to_int(height)

print(f"{size_bmp_int=}")
print(f"{offset_int=}")

print(f"{width_int=}")
print(f"{height_int=}")

new_bmp = b""
# copy the header
new_bmp += original_bmp[:offset_int]

new_bmp += bytes([0x00]) * len(original_bmp[offset_int:])

with open("blank_bmp.bmp", "wb") as f:
    f.write(new_bmp)

rotated_bmp = b""
rotated_bmp += original_bmp[:offset_int]

# columns become rows

# the first pixel is at 0,0 axis i.e. 138,139,140 bytes
# second pixel (first row, second column) is at 0,1 i.e. 141,142,143 bytes
# sixth pixel (first row, sixth column) at 0,5 i.e. 153, 154, 155 bytes
# first row, last column at 0, 419 i.e. 1395, 1396, 1397
# second row, first column at 1,0 at 138+420*3 = 1398, 1399, 1400

# new first row will be 138, 139, 140, 1398, 1399, 1400, 2658, 2659, 2660

# i.e. at offset_int + (420*3*0) : offset_int+ (420*0) + 2, offset_int + (420*1) : offset_int + (420*1) + 2
barray = []
for j in range(width_int - 1, -1, -1):
    for i in range(height_int):
        n = offset_int + (height_int * 3 * i) + (j * 3)
        barray.append(original_bmp[n])
        barray.append(original_bmp[n + 1])
        barray.append(original_bmp[n + 2])

rotated_bytes = bytes(barray)

with open("rotated_teapot.bmp", "wb") as f:
    f.write(rotated_bmp)
    f.write(rotated_bytes)
