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


def conceal_oz(message: str) -> float:
    """
    Conceal a message in the significand of a nan
    """
    bs = message.encode("utf-8")
    n = len(bs)
    if n > 6:
        raise ValueError("Message must be less than 6 bytes")

    first = b"\x7f"  # first nibble (0111) next nibble is 1111 - accounts for 7 exp bits. need the next 4 exp bits

    second = (0xF8 ^ n).to_bytes(
        1, "big"
    )  # next 4 exp bits are 1111 (f), then we have 1 (1000 = 8), followed by the length in the next 3 bits
    # ^ is an xor to add the length

    # now encode the message (48 bits)

    padding = b"\x00" * (6 - n)
    payload = bs

    return struct.unpack(">d", first + second + padding + payload)[0]


def extract(x):
    # get bytes back from packing to bytes
    bs = struct.pack(">d", x)

    n = len(bs)

    length_message = bs[1] & 0x07  # get length back, bitmask 0111

    ind = n - length_message

    return bs[ind:].decode("utf-8")


concealed_message = conceal_oz("hello")

print(concealed_message)

print(extract(concealed_message))

# print(type(concealed_message))

# print(decode(concealed_message))
