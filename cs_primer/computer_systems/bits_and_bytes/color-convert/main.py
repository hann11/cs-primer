import re
import sys

hex_dec_map = dict(zip("0123456789abcdef", range(16)))


def convert_hex_to_dec(hex_xx: str) -> int:
    return (hex_dec_map[hex_xx[0]] << 4) + hex_dec_map[
        hex_xx[1]
    ]  # shift by 4 bits or multiply by 16


def convert_hex_rgb(hex: str) -> str:
    """
    Takes in a hex string like #aabbcc and converts to 3 integers based on the 3 bytes
    """
    hex = hex.strip("#")

    r_int = convert_hex_to_dec(hex[:2])
    g_int = convert_hex_to_dec(hex[2:4])
    b_int = convert_hex_to_dec(hex[4:6])

    return f"rgb({r_int} {g_int} {b_int})"


def transform_match(match: re.Match):
    hex = match.group(1)

    return convert_hex_rgb(hex)


if __name__ == "__main__":
    input = sys.stdin.read()
    print(re.sub(r"#([0-9a-fA-F]{6})", transform_match, input))
