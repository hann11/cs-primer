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
        )  # num & 0x7f isolates the lower 7bits of the number .. 0x80 adds the msb (10000000)
        num >>= 7  # bit shift 7 places ( we encode 7 bits at a time )

    # don't add msb as no more bytes to add after this
    byte_array.append(num & 0x7F)

    return bytes(byte_array)


def decode(byte_input: bytes) -> int:
    """
    Reverse encoding. Need to do it in little endian order because encode was big endian?
    """
    # take first byte, drop msb, take 7bits, then shift 7 across.
    n = 0
    for b in reversed(byte_input):  # do it in little endian order.
        n <<= 7
        n |= (
            b & 0x7F
        )  # take away the msb. this is  a bit addition keeps the same when 1

    return n


def encode_oz(num: int) -> bytes:
    """
    Oz's implementation of varint encoding
    """
    out = []
    while num > 0:
        part = num % 128  # TODO: bitmask for speed
        num >>= 7
        if num > 0:
            part |= 0x80
        out.append(part)

    return bytes(out)


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


def read_uint64(filepath: str) -> bytes:
    """
    Read an unsigned 64-bit integer from a file.
    """
    with open(filepath, "rb") as f:
        uint64 = f.read()

    return uint64


if __name__ == "__main__":
    num = 150
    print(encode(num))
    print(encode_oz(num))
    print(encode_binary(num))
    print(decode(encode(num)))
