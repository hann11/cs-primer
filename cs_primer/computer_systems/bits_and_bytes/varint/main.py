def encode(num: int) -> bytes:
    """
    Encode an integer into a variable-length byte array.
    Follows protocol buffers' varint encoding.
    """
    # given the integer, do something and extract 7 bits and the msb
    # then shift 7 bits

    byte_array = []

    while num > 0x7F:  # 128 in hex
        # add the msb and the 7 bits??
        byte_array.append(
            (num & 0x7F) | 0x80
        )  # num & 0x7f isolates the lower 7bits of the number ..
        num >>= 7  # bit shift 7 places

    # don't add msb
    byte_array.append(num & 0x7F)

    return bytes(byte_array)


def encode_oz(num: int) -> bytes:
    pass


def encode_binary(num: int) -> str:
    """
    Encode an integer into a variable-length binary string.
    Follows protocol buffers' varint encoding.
    """
    binary_string = ""

    while num > 0x7F:  # 128 in hex
        # Add the msb and the 7 bits
        binary_string += format((num & 0x7F) | 0x80, "08b")
        num >>= 7  # Bit shift 7 places

    binary_string += " " + format(num & 0x7F, "08b")

    return binary_string


def read_varint(filepath: str) -> bytes:
    """
    Read a varint-encoded integer from a file.
    """
    with open(filepath, "rb") as f:
        varint = f.read()

    return varint


if __name__ == "__main__":
    num = 150
    print(encode(num))
    print(encode_binary(num))
