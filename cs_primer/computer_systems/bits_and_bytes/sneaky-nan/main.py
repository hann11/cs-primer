# in ieee754, a nan is represented by
# 0 11111111111 and at least one 1 in the significand
# (sign 1 bit) (exponent 11 bit) (significand 52 bit)

# so we could encode a message in the significand in binary.

import struct


def conceal(message: str) -> float:
    """
    Conceal a message in the significand of a nan
    """
    # convert message to binary and pad to 52 bits

    base_ieee754 = "011111111111"

    # convert message to hex, to int, to binary
    hexed_message = message.encode("utf-8").hex()
    hexed_message_int = int(hexed_message, 16)
    bined_message = bin(hexed_message_int)[2:]

    # pad to 52 bits and add the ieee754 base
    concealed_message = base_ieee754 + bined_message.zfill(52)

    # now want to convert to float
    int_value = int(concealed_message, 2)
    byteval = int_value.to_bytes(8, byteorder="big")
    return struct.unpack(">d", byteval)[0]


def decode(concealed_message: float) -> str:
    # convert to binary, remove the ieee754 base, convert to int, convert to hex, convert to bytes, decode
    byteval = struct.pack(">d", concealed_message)

    int_value = int.from_bytes(byteval, byteorder="big")

    bined = bin(int_value)

    bined = bined[13:]

    while bined[0] == "0":
        bined = bined[1:]

    bined_int = int(bined, 2)

    hexed = hex(bined_int)[2:]

    hex_bytes = bytes.fromhex(hexed)

    return hex_bytes.decode("utf-8")


concealed_message = conceal("hello")

print(type(concealed_message))

print(decode(concealed_message))
