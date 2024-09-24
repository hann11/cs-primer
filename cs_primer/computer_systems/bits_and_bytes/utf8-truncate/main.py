with open("cases", "rb") as f:
    transformed = b""
    for line in f:
        # drop the trailing newline

        line = line[:-1]

        trunc_length = int(line[0])

        # remove the n_bytes to truncate
        line = line[1:]

        if trunc_length < len(line):
            while (
                line[trunc_length] & 0xC0 == 0x80
            ):  # if the byte is a continuation byte, drop it to prevent invalid utf-8
                trunc_length -= 1

        newline = line[:trunc_length]

        transformed += newline + b"\x0a"

with open("truncated", "wb") as f:
    f.write(transformed)
