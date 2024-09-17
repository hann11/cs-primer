# in ieee754, a nan is represented by
# 0 11111111111 and at least one 1 in the significand
# (sign 1 bit) (exponent 11 bit) (significand 52 bit)

# so we could encode a message in the significand in binary.


def conceal(message: str) -> float:
    # convert message to binary and pad to 52 bits

    base_ieee754 = b"\b011111111111"

    hexed_message = message.encode("utf-8")

    hexed_message_int = int(hexed_message, 16)

    bined_message = bin(hexed_message_int)[2:]

    concealed_message = base_ieee754

    bined_message

    concealed_message

    return


# return the binary
